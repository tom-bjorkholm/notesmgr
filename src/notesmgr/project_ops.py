#! /usr/local/bin/python3
"""Opening a folder of notes as a notesmgr project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
from pathlib import Path
from typing import Callable, NamedTuple, Optional, Sequence
from send2trash import send2trash
from notesmgr.config import NotesmgrConfig
from notesmgr.config_files import user_wide_config, write_config_file
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import sorted_names, template_name
from notesmgr.order_file import repair_order_file
from notesmgr.project import Folder, FolderContent, Project, config_path, \
    folder_content, is_project, read_config

ALREADY_PROJECT = 'The folder {folder} is a notesmgr project already.'
"""What is said about a folder that is not to be made a project twice."""

UNRESOLVED = 'The folder {folder} holds more than one template.'
"""What is said when the user did not say which template to keep."""

NOT_TRASHED = 'The template {path} cannot be moved to the trash.\n{reason}'
"""What is said about a template too many that cannot be trashed."""

NOT_RENAMED = 'The template {path} cannot be renamed.\n{reason}'
"""What is said about a template that cannot be given the right name."""

NOT_CREATED = 'The template {path} cannot be written.\n{reason}'
"""What is said about a template that a folder lacks and cannot get."""

RENAMED_HEAD = 'Templates given the file extension of the project:'
"""Heading over the templates that opening the project renamed."""

CREATED_HEAD = 'Templates written in folders that had none:'
"""Heading over the templates that opening the project created."""


class OpenReport(NamedTuple):
    """An opened project, and what opening it did to the files.

    Opening a project repairs what it finds, so the user is told what
    was changed and what could not be done, rather than finding it out
    later from the file system.
    """

    project: Project
    renamed: Sequence[Path]
    created: Sequence[Path]
    problems: Sequence[str]


class ProjectOpener:
    """Reads a project folder, repairing what it finds on the way.

    Every folder of a project holds one template carrying the file
    extension of the project, and a note order file listing the notes
    that are really there. This makes that true as the tree is read.

    Which of several templates in one folder is the one to keep is the
    only question with no right answer, so a chooser is asked, and an
    answer of None refuses to open the project at all. Everything else
    that cannot be done is gathered as a problem to be reported, and
    the rest of the project is still opened.
    """

    def __init__(self, root: Path, config: NotesmgrConfig,
                 chooser: Callable[[Path, Sequence[Path]],
                                   Optional[Path]]) -> None:
        """Get ready to read the project in a folder.

        Args:
            root: The root folder of the project.
            config: The configuration that the project is used with.
            chooser: Asked which of the templates of a folder is the
                one to keep, whenever a folder holds more than one.
        """
        self.root = root
        self.config = config
        self.chooser = chooser
        self.renamed: list[Path] = []
        self.created: list[Path] = []
        self.problems: list[str] = []

    def read(self) -> OpenReport:
        """Return the project, having repaired what needed repair.

        Raises:
            NotesmgrError: A folder holds several templates, and the
                user did not say which of them to keep.
        """
        tree = self.folder(self.root, None)
        project = Project(root=self.root, config=self.config, tree=tree)
        return OpenReport(project=project, renamed=self.renamed,
                          created=self.created, problems=self.problems)

    def folder(self, folder: Path, parent: Optional[Path]) -> Folder:
        """Return one folder of the tree, and everything below it.

        Args:
            folder: The folder to read.
            parent: Template of the folder above, None in the root.

        Returns:
            The folder as it is shown, and empty when it cannot be
            read at all, which is reported as a problem instead.
        """
        try:
            content = folder_content(folder)
        except NotesmgrError as error:
            self.problems.append(str(error))
            return Folder(path=folder, folders=[], template=None, notes=[])
        return self.repaired(folder, content, parent)

    def repaired(self, folder: Path, content: FolderContent,
                 parent: Optional[Path]) -> Folder:
        """Return a folder whose template and note order are in order."""
        template = self.template(folder, content.templates, parent)
        notes = self.notes(folder, content.notes)
        below = [self.folder(path, template) for path in content.folders]
        return Folder(path=folder, folders=below, template=template,
                      notes=notes)

    def notes(self, folder: Path, names: Sequence[str]) -> list[Path]:
        """Return the notes of a folder in the order they are shown in.

        A note order file that cannot be read or written is reported,
        and its folder is then shown in alphabetical order instead.
        """
        try:
            order = repair_order_file(folder, names)
        except NotesmgrError as error:
            self.problems.append(str(error))
            order = sorted_names(names)
        return [folder / name for name in order]

    def template(self, folder: Path, templates: Sequence[Path],
                 parent: Optional[Path]) -> Optional[Path]:
        """Return the one template of a folder, making it the only one.

        Args:
            folder: The folder the template belongs to.
            templates: The templates that the folder holds now.
            parent: Template of the folder above, None in the root.

        Returns:
            The template of the folder, None when it has none and
            none could be written.

        Raises:
            NotesmgrError: The folder holds several templates, and the
                user did not say which of them to keep.
        """
        kept = self.kept_template(folder, templates)
        if kept is None:
            return self.new_template(folder, parent)
        return self.rightly_named(kept)

    def kept_template(self, folder: Path,
                      templates: Sequence[Path]) -> Optional[Path]:
        """Return the template to keep, trashing the ones too many.

        Raises:
            NotesmgrError: There are several templates, and the user
                did not say which of them to keep.
        """
        if len(templates) < 2:
            return templates[0] if templates else None
        keep = self.chooser(folder, templates)
        if keep is None:
            raise NotesmgrError(UNRESOLVED.format(folder=folder))
        for path in templates:
            if path != keep:
                self.trash_template(path)
        return keep

    def trash_template(self, path: Path) -> None:
        """Move a template that is one too many to the trash."""
        try:
            send2trash(path)
        except OSError as error:
            self.problems.append(NOT_TRASHED.format(path=path, reason=error))

    def rightly_named(self, kept: Path) -> Path:
        """Return the template, named with the extension of the project.

        Args:
            kept: The template of the folder as it is named now.

        Returns:
            The template under the name it is to have, and under the
            name it had when it could not be renamed.
        """
        wanted = kept.parent / template_name(self.config.file_extension)
        if wanted == kept:
            return kept
        try:
            kept.rename(wanted)
        except OSError as error:
            self.problems.append(NOT_RENAMED.format(path=kept, reason=error))
            return kept
        self.renamed.append(wanted)
        return wanted

    def new_template(self, folder: Path,
                     parent: Optional[Path]) -> Optional[Path]:
        """Return a template written in a folder that held none.

        The root folder of a project gets an empty template, and a
        folder below it gets a copy of the template of the folder
        above it, so that a new folder starts out as its parent does.

        Args:
            folder: The folder that is to get a template.
            parent: Template of the folder above, None in the root.

        Returns:
            The template that was written, None when it could not be,
            which is reported as a problem instead.
        """
        wanted = folder / template_name(self.config.file_extension)
        try:
            if parent is None:
                wanted.write_text('', encoding='utf-8')
            else:
                shutil.copyfile(parent, wanted)
        except OSError as error:
            self.problems.append(NOT_CREATED.format(path=wanted, reason=error))
            return None
        self.created.append(wanted)
        return wanted


def open_project(root: Path,
                 chooser: Callable[[Path, Sequence[Path]],
                                   Optional[Path]]) -> OpenReport:
    """Open the project in a folder, repairing what needs repair.

    Args:
        root: The root folder of the project.
        chooser: Asked which of the templates of a folder is the one
            to keep, whenever a folder holds more than one.

    Returns:
        The project, and what opening it changed on the way.

    Raises:
        NotesmgrError: The folder is no project, its configuration
            cannot be used, or a template was not chosen.
    """
    return ProjectOpener(root, read_config(root), chooser).read()


def create_project(root: Path,
                   chooser: Callable[[Path, Sequence[Path]],
                                     Optional[Path]]) -> OpenReport:
    """Make a folder into a project, and open it.

    The notes that the folder holds already become the notes of the
    project, in alphabetical order, and the configuration of the
    project starts out as a copy of the user wide configuration.

    Args:
        root: The folder to make into a project.
        chooser: Asked which of the templates of a folder is the one
            to keep, whenever a folder holds more than one.

    Returns:
        The project, and what making it wrote on the way.

    Raises:
        NotesmgrError: The folder is a project already, or its
            configuration file cannot be written.
    """
    if is_project(root):
        raise NotesmgrError(ALREADY_PROJECT.format(folder=root))
    config = user_wide_config()
    write_config_file(config, config_path(root))
    return ProjectOpener(root, config, chooser).read()


def named_list(head: str, paths: Sequence[Path]) -> str:
    """Return a heading with the paths below it, nothing for no paths."""
    if not paths:
        return ''
    listed = '\n'.join(f'    {path}' for path in paths)
    return f'{head}\n{listed}\n'


def changed_message(report: OpenReport) -> str:
    """Return what to tell the user that opening a project changed.

    Args:
        report: What opening the project gave.

    Returns:
        What to tell, and nothing at all when nothing was changed.
    """
    return named_list(RENAMED_HEAD, report.renamed) + \
        named_list(CREATED_HEAD, report.created)

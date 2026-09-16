# Table of Contents

* [notesmgr.main\_window](#notesmgr.main_window)
  * [Shortcut](#notesmgr.main_window.Shortcut)
  * [tk\_window\_system](#notesmgr.main_window.tk_window_system)
  * [quit\_shortcut](#notesmgr.main_window.quit_shortcut)
  * [MainWindow](#notesmgr.main_window.MainWindow)
    * [\_\_init\_\_](#notesmgr.main_window.MainWindow.__init__)
    * [\_menu\_specs](#notesmgr.main_window.MainWindow._menu_specs)
    * [\_note\_entries](#notesmgr.main_window.MainWindow._note_entries)
    * [\_folder\_entries](#notesmgr.main_window.MainWindow._folder_entries)
    * [\_bind\_quit\_shortcut](#notesmgr.main_window.MainWindow._bind_quit_shortcut)
    * [\_shape\_window](#notesmgr.main_window.MainWindow._shape_window)
    * [show\_project](#notesmgr.main_window.MainWindow.show_project)
    * [show\_selected](#notesmgr.main_window.MainWindow.show_selected)
    * [offer\_actions](#notesmgr.main_window.MainWindow.offer_actions)
    * [new\_project\_dialog](#notesmgr.main_window.MainWindow.new_project_dialog)
    * [open\_project\_dialog](#notesmgr.main_window.MainWindow.open_project_dialog)
    * [load\_project](#notesmgr.main_window.MainWindow.load_project)
    * [make\_project](#notesmgr.main_window.MainWindow.make_project)
    * [reopen](#notesmgr.main_window.MainWindow.reopen)
    * [opened](#notesmgr.main_window.MainWindow.opened)
    * [choose\_template](#notesmgr.main_window.MainWindow.choose_template)
    * [show\_opened](#notesmgr.main_window.MainWindow.show_opened)
    * [select](#notesmgr.main_window.MainWindow.select)
    * [tell\_about\_opening](#notesmgr.main_window.MainWindow.tell_about_opening)
    * [edit\_configuration](#notesmgr.main_window.MainWindow.edit_configuration)
    * [\_config\_closed](#notesmgr.main_window.MainWindow._config_closed)
    * [save\_user\_wide](#notesmgr.main_window.MainWindow.save_user_wide)
    * [show\_version](#notesmgr.main_window.MainWindow.show_version)
    * [quit](#notesmgr.main_window.MainWindow.quit)
* [notesmgr.version\_info](#notesmgr.version_info)
  * [MAIN\_PACKAGE](#notesmgr.version_info.MAIN_PACKAGE)
  * [REPORTED\_PACKAGES](#notesmgr.version_info.REPORTED_PACKAGES)
  * [RECOMMENDED\_PYTHON](#notesmgr.version_info.RECOMMENDED_PYTHON)
  * [SUPPORT\_EXPIRES](#notesmgr.version_info.SUPPORT_EXPIRES)
  * [NotesmgrVersions](#notesmgr.version_info.NotesmgrVersions)
    * [package\_names](#notesmgr.version_info.NotesmgrVersions.package_names)
    * [get\_app\_support\_expires](#notesmgr.version_info.NotesmgrVersions.get_app_support_expires)
    * [get\_main\_package\_name](#notesmgr.version_info.NotesmgrVersions.get_main_package_name)
    * [recommended\_python](#notesmgr.version_info.NotesmgrVersions.recommended_python)
  * [version\_report](#notesmgr.version_info.version_report)
* [notesmgr.menu\_bar](#notesmgr.menu_bar)
  * [MenuEntry](#notesmgr.menu_bar.MenuEntry)
  * [MenuSpec](#notesmgr.menu_bar.MenuSpec)
  * [MenuBar](#notesmgr.menu_bar.MenuBar)
  * [entry\_state](#notesmgr.menu_bar.entry_state)
  * [build\_menu](#notesmgr.menu_bar.build_menu)
  * [build\_menu\_bar](#notesmgr.menu_bar.build_menu_bar)
  * [set\_enabled](#notesmgr.menu_bar.set_enabled)
  * [entry\_labels](#notesmgr.menu_bar.entry_labels)
* [notesmgr.cmd\_line](#notesmgr.cmd_line)
  * [PROGRAM\_NAME](#notesmgr.cmd_line.PROGRAM_NAME)
  * [DESCRIPTION](#notesmgr.cmd_line.DESCRIPTION)
  * [FOLDER\_HELP](#notesmgr.cmd_line.FOLDER_HELP)
  * [VERSION\_HELP](#notesmgr.cmd_line.VERSION_HELP)
  * [CommandLine](#notesmgr.cmd_line.CommandLine)
  * [argument\_parser](#notesmgr.cmd_line.argument_parser)
  * [parse\_command\_line](#notesmgr.cmd_line.parse_command_line)
* [notesmgr.editor\_command](#notesmgr.editor_command)
  * [PLACEHOLDER](#notesmgr.editor_command.PLACEHOLDER)
  * [ON\_WINDOWS](#notesmgr.editor_command.ON_WINDOWS)
  * [QUOTES](#notesmgr.editor_command.QUOTES)
  * [UNREADABLE](#notesmgr.editor_command.UNREADABLE)
  * [NO\_PROGRAM](#notesmgr.editor_command.NO_PROGRAM)
  * [NOT\_STARTED](#notesmgr.editor_command.NOT_STARTED)
  * [unquoted](#notesmgr.editor_command.unquoted)
  * [split\_command](#notesmgr.editor_command.split_command)
  * [editor\_argv](#notesmgr.editor_command.editor_argv)
  * [start\_detached](#notesmgr.editor_command.start_detached)
  * [launch\_editor](#notesmgr.editor_command.launch_editor)
* [notesmgr.config](#notesmgr.config)
  * [EMPTY\_EDITOR](#notesmgr.config.EMPTY_EDITOR)
  * [NoteExtension](#notesmgr.config.NoteExtension)
  * [DEFAULT\_EXTENSION](#notesmgr.config.DEFAULT_EXTENSION)
  * [DEFAULT\_NOTE\_SIZE](#notesmgr.config.DEFAULT_NOTE_SIZE)
  * [MIN\_NOTE\_SIZE](#notesmgr.config.MIN_NOTE_SIZE)
  * [MAX\_NOTE\_SIZE](#notesmgr.config.MAX_NOTE_SIZE)
  * [OldNotesmgrConfig](#notesmgr.config.OldNotesmgrConfig)
    * [get\_missing\_path\_values](#notesmgr.config.OldNotesmgrConfig.get_missing_path_values)
  * [NotesmgrConfig](#notesmgr.config.NotesmgrConfig)
    * [\_\_init\_\_](#notesmgr.config.NotesmgrConfig.__init__)
    * [\_get\_read\_old\_config](#notesmgr.config.NotesmgrConfig._get_read_old_config)
    * [parse\_converters](#notesmgr.config.NotesmgrConfig.parse_converters)
    * [get\_validation\_plan](#notesmgr.config.NotesmgrConfig.get_validation_plan)
    * [stripped\_editor](#notesmgr.config.NotesmgrConfig.stripped_editor)
* [notesmgr.note\_ops](#notesmgr.note_ops)
  * [NAME\_TAKEN](#notesmgr.note_ops.NAME_TAKEN)
  * [NOT\_WRITTEN](#notesmgr.note_ops.NOT_WRITTEN)
  * [NOT\_COPIED](#notesmgr.note_ops.NOT_COPIED)
  * [NOT\_TRASHED](#notesmgr.note_ops.NOT_TRASHED)
  * [resync\_order](#notesmgr.note_ops.resync_order)
  * [free\_path](#notesmgr.note_ops.free_path)
  * [new\_path](#notesmgr.note_ops.new_path)
  * [template\_text](#notesmgr.note_ops.template_text)
  * [new\_note](#notesmgr.note_ops.new_note)
  * [duplicate\_note](#notesmgr.note_ops.duplicate_note)
  * [delete\_note](#notesmgr.note_ops.delete_note)
  * [moved\_order](#notesmgr.note_ops.moved_order)
  * [move\_note](#notesmgr.note_ops.move_note)
* [notesmgr.session](#notesmgr.session)
  * [start\_folder](#notesmgr.session.start_folder)
  * [Session](#notesmgr.session.Session)
    * [\_\_init\_\_](#notesmgr.session.Session.__init__)
    * [opened](#notesmgr.session.Session.opened)
    * [chooser\_folder](#notesmgr.session.Session.chooser_folder)
    * [config\_file](#notesmgr.session.Session.config_file)
    * [config](#notesmgr.session.Session.config)
* [notesmgr.actions](#notesmgr.actions)
  * [COPY\_RAW](#notesmgr.actions.COPY_RAW)
  * [COPY\_FORMATTED](#notesmgr.actions.COPY_FORMATTED)
  * [DUPLICATE](#notesmgr.actions.DUPLICATE)
  * [EDIT](#notesmgr.actions.EDIT)
  * [NEW](#notesmgr.actions.NEW)
  * [DELETE](#notesmgr.actions.DELETE)
  * [MOVE\_UP](#notesmgr.actions.MOVE_UP)
  * [MOVE\_DOWN](#notesmgr.actions.MOVE_DOWN)
  * [NEW\_FOLDER](#notesmgr.actions.NEW_FOLDER)
  * [RENAME\_FOLDER](#notesmgr.actions.RENAME_FOLDER)
  * [DELETE\_FOLDER](#notesmgr.actions.DELETE_FOLDER)
  * [ON\_NOTE](#notesmgr.actions.ON_NOTE)
  * [ON\_PLAIN](#notesmgr.actions.ON_PLAIN)
  * [ON\_PROJECT](#notesmgr.actions.ON_PROJECT)
  * [ON\_FOLDER](#notesmgr.actions.ON_FOLDER)
  * [Selected](#notesmgr.actions.Selected)
  * [NOTHING](#notesmgr.actions.NOTHING)
  * [offered](#notesmgr.actions.offered)
* [notesmgr.config\_files](#notesmgr.config_files)
  * [CONFIG\_VARIABLE](#notesmgr.config_files.CONFIG_VARIABLE)
  * [CONFIG\_NAME](#notesmgr.config_files.CONFIG_NAME)
  * [MISSING](#notesmgr.config_files.MISSING)
  * [NOT\_READ](#notesmgr.config_files.NOT_READ)
  * [NOT\_WRITTEN](#notesmgr.config_files.NOT_WRITTEN)
  * [user\_config\_path](#notesmgr.config_files.user_config_path)
  * [user\_config\_source](#notesmgr.config_files.user_config_source)
  * [copy\_to\_user\_wide](#notesmgr.config_files.copy_to_user_wide)
  * [config\_error](#notesmgr.config_files.config_error)
  * [read\_config\_file](#notesmgr.config_files.read_config_file)
  * [write\_config\_file](#notesmgr.config_files.write_config_file)
  * [user\_wide\_config](#notesmgr.config_files.user_wide_config)
* [notesmgr.button\_row](#notesmgr.button_row)
  * [GAP](#notesmgr.button_row.GAP)
  * [ButtonSpec](#notesmgr.button_row.ButtonSpec)
  * [grid\_width](#notesmgr.button_row.grid_width)
  * [fitting\_columns](#notesmgr.button_row.fitting_columns)
  * [ButtonRow](#notesmgr.button_row.ButtonRow)
    * [\_\_init\_\_](#notesmgr.button_row.ButtonRow.__init__)
    * [\_built](#notesmgr.button_row.ButtonRow._built)
    * [\_width\_changed](#notesmgr.button_row.ButtonRow._width_changed)
    * [widths](#notesmgr.button_row.ButtonRow.widths)
    * [fit\_into](#notesmgr.button_row.ButtonRow.fit_into)
    * [lay\_out](#notesmgr.button_row.ButtonRow.lay_out)
    * [offer](#notesmgr.button_row.ButtonRow.offer)
* [notesmgr.config\_editor](#notesmgr.config_editor)
  * [editor\_files](#notesmgr.config_editor.editor_files)
  * [open\_config\_editor](#notesmgr.config_editor.open_config_editor)
* [notesmgr.application](#notesmgr.application)
  * [main](#notesmgr.application.main)
* [notesmgr.trash](#notesmgr.trash)
  * [send\_to\_trash](#notesmgr.trash.send_to_trash)
* [notesmgr.config\_defaults](#notesmgr.config_defaults)
  * [VISUAL\_CODE](#notesmgr.config_defaults.VISUAL_CODE)
  * [VISUAL\_CODE\_FLAG](#notesmgr.config_defaults.VISUAL_CODE_FLAG)
  * [EDITOR\_VARIABLE](#notesmgr.config_defaults.EDITOR_VARIABLE)
  * [PLATFORM\_EDITORS](#notesmgr.config_defaults.PLATFORM_EDITORS)
  * [OTHER\_EDITOR](#notesmgr.config_defaults.OTHER_EDITOR)
  * [default\_editor](#notesmgr.config_defaults.default_editor)
* [notesmgr.note\_panel](#notesmgr.note_panel)
  * [PADDING](#notesmgr.note_panel.PADDING)
  * [NotePanel](#notesmgr.note_panel.NotePanel)
    * [\_\_init\_\_](#notesmgr.note_panel.NotePanel.__init__)
    * [\_button\_specs](#notesmgr.note_panel.NotePanel._button_specs)
    * [actions](#notesmgr.note_panel.NotePanel.actions)
    * [note\_limit](#notesmgr.note_panel.NotePanel.note_limit)
    * [note\_path](#notesmgr.note_panel.NotePanel.note_path)
    * [has\_note](#notesmgr.note_panel.NotePanel.has_note)
    * [show\_path](#notesmgr.note_panel.NotePanel.show_path)
    * [reload](#notesmgr.note_panel.NotePanel.reload)
    * [offer](#notesmgr.note_panel.NotePanel.offer)
    * [shown\_path](#notesmgr.note_panel.NotePanel.shown_path)
    * [edit\_note](#notesmgr.note_panel.NotePanel.edit_note)
    * [copy\_raw](#notesmgr.note_panel.NotePanel.copy_raw)
* [notesmgr.project\_ops](#notesmgr.project_ops)
  * [ALREADY\_PROJECT](#notesmgr.project_ops.ALREADY_PROJECT)
  * [UNRESOLVED](#notesmgr.project_ops.UNRESOLVED)
  * [NOT\_TRASHED](#notesmgr.project_ops.NOT_TRASHED)
  * [NOT\_RENAMED](#notesmgr.project_ops.NOT_RENAMED)
  * [NOT\_CREATED](#notesmgr.project_ops.NOT_CREATED)
  * [RENAMED\_HEAD](#notesmgr.project_ops.RENAMED_HEAD)
  * [CREATED\_HEAD](#notesmgr.project_ops.CREATED_HEAD)
  * [OpenReport](#notesmgr.project_ops.OpenReport)
  * [ProjectOpener](#notesmgr.project_ops.ProjectOpener)
    * [\_\_init\_\_](#notesmgr.project_ops.ProjectOpener.__init__)
    * [read](#notesmgr.project_ops.ProjectOpener.read)
    * [folder](#notesmgr.project_ops.ProjectOpener.folder)
    * [repaired](#notesmgr.project_ops.ProjectOpener.repaired)
    * [notes](#notesmgr.project_ops.ProjectOpener.notes)
    * [template](#notesmgr.project_ops.ProjectOpener.template)
    * [kept\_template](#notesmgr.project_ops.ProjectOpener.kept_template)
    * [trash\_template](#notesmgr.project_ops.ProjectOpener.trash_template)
    * [rightly\_named](#notesmgr.project_ops.ProjectOpener.rightly_named)
    * [new\_template](#notesmgr.project_ops.ProjectOpener.new_template)
  * [open\_project](#notesmgr.project_ops.open_project)
  * [create\_project](#notesmgr.project_ops.create_project)
  * [named\_list](#notesmgr.project_ops.named_list)
  * [changed\_message](#notesmgr.project_ops.changed_message)
* [notesmgr.order\_file](#notesmgr.order_file)
  * [ORDER\_NAME](#notesmgr.order_file.ORDER_NAME)
  * [WRITING\_NAME](#notesmgr.order_file.WRITING_NAME)
  * [NOT\_READ](#notesmgr.order_file.NOT_READ)
  * [NOT\_WRITTEN](#notesmgr.order_file.NOT_WRITTEN)
  * [order\_path](#notesmgr.order_file.order_path)
  * [read\_order\_text](#notesmgr.order_file.read_order_text)
  * [names\_a\_file](#notesmgr.order_file.names_a_file)
  * [parse\_order](#notesmgr.order_file.parse_order)
  * [repair\_order](#notesmgr.order_file.repair_order)
  * [order\_text](#notesmgr.order_file.order_text)
  * [write\_order](#notesmgr.order_file.write_order)
  * [repair\_order\_file](#notesmgr.order_file.repair_order_file)
* [notesmgr.explorer\_tree](#notesmgr.explorer_tree)
  * [EXPLORER\_WIDTH](#notesmgr.explorer_tree.EXPLORER_WIDTH)
  * [SELECT\_EVENT](#notesmgr.explorer_tree.SELECT_EVENT)
  * [ExplorerTree](#notesmgr.explorer_tree.ExplorerTree)
    * [\_\_init\_\_](#notesmgr.explorer_tree.ExplorerTree.__init__)
    * [selection\_changed](#notesmgr.explorer_tree.ExplorerTree.selection_changed)
    * [selected\_path](#notesmgr.explorer_tree.ExplorerTree.selected_path)
    * [select](#notesmgr.explorer_tree.ExplorerTree.select)
    * [show](#notesmgr.explorer_tree.ExplorerTree.show)
    * [add\_folder](#notesmgr.explorer_tree.ExplorerTree.add_folder)
    * [shown\_files](#notesmgr.explorer_tree.ExplorerTree.shown_files)
* [notesmgr.errors](#notesmgr.errors)
  * [NotesmgrError](#notesmgr.errors.NotesmgrError)
* [notesmgr.dialogs](#notesmgr.dialogs)
  * [MIN\_TEXT\_WIDTH](#notesmgr.dialogs.MIN_TEXT_WIDTH)
  * [MAX\_TEXT\_WIDTH](#notesmgr.dialogs.MAX_TEXT_WIDTH)
  * [MAX\_TEXT\_HEIGHT](#notesmgr.dialogs.MAX_TEXT_HEIGHT)
  * [CLOSE\_LABEL](#notesmgr.dialogs.CLOSE_LABEL)
  * [PADDING](#notesmgr.dialogs.PADDING)
  * [BUSY\_CURSOR](#notesmgr.dialogs.BUSY_CURSOR)
  * [CHOOSE\_LABEL](#notesmgr.dialogs.CHOOSE_LABEL)
  * [CANCEL\_LABEL](#notesmgr.dialogs.CANCEL_LABEL)
  * [ACCEPT\_LABEL](#notesmgr.dialogs.ACCEPT_LABEL)
  * [NAME\_LABEL](#notesmgr.dialogs.NAME_LABEL)
  * [FOLDER\_LABEL](#notesmgr.dialogs.FOLDER_LABEL)
  * [ENTRY\_WIDTH](#notesmgr.dialogs.ENTRY_WIDTH)
  * [text\_size](#notesmgr.dialogs.text_size)
  * [show\_text](#notesmgr.dialogs.show_text)
  * [\_fill\_with\_text](#notesmgr.dialogs._fill_with_text)
  * [show\_error](#notesmgr.dialogs.show_error)
  * [busy\_cursor](#notesmgr.dialogs.busy_cursor)
  * [ask\_folder](#notesmgr.dialogs.ask_folder)
  * [ask\_yes\_no](#notesmgr.dialogs.ask_yes_no)
  * [show\_info](#notesmgr.dialogs.show_info)
  * [AskingWindow](#notesmgr.dialogs.AskingWindow)
    * [\_\_init\_\_](#notesmgr.dialogs.AskingWindow.__init__)
    * [ask](#notesmgr.dialogs.AskingWindow.ask)
    * [add\_buttons](#notesmgr.dialogs.AskingWindow.add_buttons)
    * [accept](#notesmgr.dialogs.AskingWindow.accept)
    * [cancel](#notesmgr.dialogs.AskingWindow.cancel)
    * [answered](#notesmgr.dialogs.AskingWindow.answered)
  * [ChoiceDialog](#notesmgr.dialogs.ChoiceDialog)
    * [\_\_init\_\_](#notesmgr.dialogs.ChoiceDialog.__init__)
    * [chosen](#notesmgr.dialogs.ChoiceDialog.chosen)
    * [choose](#notesmgr.dialogs.ChoiceDialog.choose)
  * [ask\_choice](#notesmgr.dialogs.ask_choice)
  * [ask\_name](#notesmgr.dialogs.ask_name)
  * [NameFolder](#notesmgr.dialogs.NameFolder)
  * [NameFolderDialog](#notesmgr.dialogs.NameFolderDialog)
    * [\_\_init\_\_](#notesmgr.dialogs.NameFolderDialog.__init__)
    * [\_fill\_in](#notesmgr.dialogs.NameFolderDialog._fill_in)
    * [given](#notesmgr.dialogs.NameFolderDialog.given)
    * [ask\_for](#notesmgr.dialogs.NameFolderDialog.ask_for)
  * [ask\_name\_folder](#notesmgr.dialogs.ask_name_folder)
* [notesmgr.note\_text](#notesmgr.note_text)
  * [NOT\_UTF8](#notesmgr.note_text.NOT_UTF8)
  * [NOT\_READ](#notesmgr.note_text.NOT_READ)
  * [TOO\_LONG](#notesmgr.note_text.TOO_LONG)
  * [NoteText](#notesmgr.note_text.NoteText)
  * [EMPTY\_NOTE](#notesmgr.note_text.EMPTY_NOTE)
  * [read\_note\_text](#notesmgr.note_text.read_note_text)
* [notesmgr.file\_watch](#notesmgr.file_watch)
  * [POLL\_INTERVAL](#notesmgr.file_watch.POLL_INTERVAL)
  * [FileState](#notesmgr.file_watch.FileState)
  * [MISSING](#notesmgr.file_watch.MISSING)
  * [file\_state](#notesmgr.file_watch.file_state)
  * [FileWatch](#notesmgr.file_watch.FileWatch)
    * [\_\_init\_\_](#notesmgr.file_watch.FileWatch.__init__)
    * [watch](#notesmgr.file_watch.FileWatch.watch)
    * [poll](#notesmgr.file_watch.FileWatch.poll)
    * [tick](#notesmgr.file_watch.FileWatch.tick)
    * [schedule](#notesmgr.file_watch.FileWatch.schedule)
    * [cancel](#notesmgr.file_watch.FileWatch.cancel)
* [notesmgr.commands](#notesmgr.commands)
  * [NOTE\_TITLE](#notesmgr.commands.NOTE_TITLE)
  * [FOLDER\_TITLE](#notesmgr.commands.FOLDER_TITLE)
  * [DUPLICATE\_TITLE](#notesmgr.commands.DUPLICATE_TITLE)
  * [ASK\_NEW\_NOTE](#notesmgr.commands.ASK_NEW_NOTE)
  * [ASK\_DELETE\_NOTE](#notesmgr.commands.ASK_DELETE_NOTE)
  * [ASK\_NEW\_FOLDER](#notesmgr.commands.ASK_NEW_FOLDER)
  * [ASK\_RENAME\_FOLDER](#notesmgr.commands.ASK_RENAME_FOLDER)
  * [ASK\_DELETE\_FOLDER](#notesmgr.commands.ASK_DELETE_FOLDER)
  * [COPY\_SUFFIX](#notesmgr.commands.COPY_SUFFIX)
  * [shown\_folder](#notesmgr.commands.shown_folder)
  * [folder\_of](#notesmgr.commands.folder_of)
  * [WindowHooks](#notesmgr.commands.WindowHooks)
  * [Commands](#notesmgr.commands.Commands)
    * [\_\_init\_\_](#notesmgr.commands.Commands.__init__)
    * [select](#notesmgr.commands.Commands.select)
    * [note\_shown](#notesmgr.commands.Commands.note_shown)
    * [selected](#notesmgr.commands.Commands.selected)
    * [report\_error](#notesmgr.commands.Commands.report_error)
    * [chosen\_folder](#notesmgr.commands.Commands.chosen_folder)
    * [note\_folder](#notesmgr.commands.Commands.note_folder)
    * [plain\_note](#notesmgr.commands.Commands.plain_note)
    * [\_extension](#notesmgr.commands.Commands._extension)
    * [done](#notesmgr.commands.Commands.done)
    * [edit](#notesmgr.commands.Commands.edit)
    * [new\_note](#notesmgr.commands.Commands.new_note)
    * [duplicate\_note](#notesmgr.commands.Commands.duplicate_note)
    * [\_ask\_copy](#notesmgr.commands.Commands._ask_copy)
    * [\_folder\_names](#notesmgr.commands.Commands._folder_names)
    * [delete\_note](#notesmgr.commands.Commands.delete_note)
    * [move\_up](#notesmgr.commands.Commands.move_up)
    * [move\_down](#notesmgr.commands.Commands.move_down)
    * [move](#notesmgr.commands.Commands.move)
    * [new\_folder](#notesmgr.commands.Commands.new_folder)
    * [rename\_folder](#notesmgr.commands.Commands.rename_folder)
    * [delete\_folder](#notesmgr.commands.Commands.delete_folder)
* [notesmgr.note\_file](#notesmgr.note_file)
  * [TEMPLATE\_STEM](#notesmgr.note_file.TEMPLATE_STEM)
  * [NOTE\_EXTENSIONS](#notesmgr.note_file.NOTE_EXTENSIONS)
  * [SEPARATORS](#notesmgr.note_file.SEPARATORS)
  * [NOT\_IN\_NAME](#notesmgr.note_file.NOT_IN_NAME)
  * [NO\_NAME](#notesmgr.note_file.NO_NAME)
  * [INVALID\_NAME](#notesmgr.note_file.INVALID_NAME)
  * [HIDDEN](#notesmgr.note_file.HIDDEN)
  * [WRONG\_EXTENSION](#notesmgr.note_file.WRONG_EXTENSION)
  * [RESERVED](#notesmgr.note_file.RESERVED)
  * [note\_extension](#notesmgr.note_file.note_extension)
  * [is\_note](#notesmgr.note_file.is_note)
  * [note\_stem](#notesmgr.note_file.note_stem)
  * [template\_name](#notesmgr.note_file.template_name)
  * [is\_template](#notesmgr.note_file.is_template)
  * [is\_plain\_note](#notesmgr.note_file.is_plain_note)
  * [name\_key](#notesmgr.note_file.name_key)
  * [sorted\_names](#notesmgr.note_file.sorted_names)
  * [checked\_extension](#notesmgr.note_file.checked_extension)
  * [checked\_name](#notesmgr.note_file.checked_name)
  * [note\_file\_name](#notesmgr.note_file.note_file_name)
* [notesmgr.note\_view](#notesmgr.note_view)
  * [WARNING\_COLOUR](#notesmgr.note_view.WARNING_COLOUR)
  * [WARNING\_FONT](#notesmgr.note_view.WARNING_FONT)
  * [WRAP\_WIDTH](#notesmgr.note_view.WRAP_WIDTH)
  * [PADDING](#notesmgr.note_view.PADDING)
  * [TEXT\_ROW](#notesmgr.note_view.TEXT_ROW)
  * [NoteView](#notesmgr.note_view.NoteView)
    * [\_\_init\_\_](#notesmgr.note_view.NoteView.__init__)
    * [\_lay\_out](#notesmgr.note_view.NoteView._lay_out)
    * [show](#notesmgr.note_view.NoteView.show)
    * [show\_warning](#notesmgr.note_view.NoteView.show_warning)
    * [show\_text](#notesmgr.note_view.NoteView.show_text)
    * [shown\_note](#notesmgr.note_view.NoteView.shown_note)
    * [area\_text](#notesmgr.note_view.NoteView.area_text)
    * [warning\_shown](#notesmgr.note_view.NoteView.warning_shown)
* [notesmgr.descriptions](#notesmgr.descriptions)
  * [DESCRIPTIONS](#notesmgr.descriptions.DESCRIPTIONS)
* [notesmgr.project](#notesmgr.project)
  * [PROJECT\_CONFIG](#notesmgr.project.PROJECT_CONFIG)
  * [NO\_PROJECT](#notesmgr.project.NO_PROJECT)
  * [NOT\_LISTED](#notesmgr.project.NOT_LISTED)
  * [FolderContent](#notesmgr.project.FolderContent)
  * [Folder](#notesmgr.project.Folder)
  * [Project](#notesmgr.project.Project)
  * [config\_path](#notesmgr.project.config_path)
  * [is\_project](#notesmgr.project.is_project)
  * [read\_config](#notesmgr.project.read_config)
  * [is\_shown\_folder](#notesmgr.project.is_shown_folder)
  * [folder\_entries](#notesmgr.project.folder_entries)
  * [folder\_content](#notesmgr.project.folder_content)
  * [folder\_paths](#notesmgr.project.folder_paths)
* [notesmgr.folder\_ops](#notesmgr.folder_ops)
  * [IS\_PROJECT](#notesmgr.folder_ops.IS_PROJECT)
  * [NOT\_EMPTY](#notesmgr.folder_ops.NOT_EMPTY)
  * [NOT\_MADE](#notesmgr.folder_ops.NOT_MADE)
  * [NOT\_RENAMED](#notesmgr.folder_ops.NOT_RENAMED)
  * [NOT\_TRASHED](#notesmgr.folder_ops.NOT_TRASHED)
  * [new\_folder](#notesmgr.folder_ops.new_folder)
  * [rename\_folder](#notesmgr.folder_ops.rename_folder)
  * [is\_empty](#notesmgr.folder_ops.is_empty)
  * [delete\_folder](#notesmgr.folder_ops.delete_folder)

<a id="notesmgr.main_window"></a>

# notesmgr.main\_window

The main window of the notesmgr application.

<a id="notesmgr.main_window.Shortcut"></a>

## Shortcut Objects

```python
class Shortcut(NamedTuple)
```

A keyboard shortcut: its Tk event sequence and its menu label.

<a id="notesmgr.main_window.tk_window_system"></a>

#### tk\_window\_system

```python
def tk_window_system(window: tkinter.Misc) -> str
```

Return the windowing system Tk uses: aqua, win32 or x11.

<a id="notesmgr.main_window.quit_shortcut"></a>

#### quit\_shortcut

```python
def quit_shortcut(window_system: str) -> Shortcut
```

Return the keyboard shortcut that closes the main window.

macOS closes a window with Cmd+W, while Windows and the X11
desktops leave a program with Ctrl+Q.

<a id="notesmgr.main_window.MainWindow"></a>

## MainWindow Objects

```python
class MainWindow()
```

The notesmgr main window with its explorer and its note panel.

The window is given to the constructor instead of created by it, so
that the application can use the Tk root window while tests can use
a hidden toplevel window under one shared Tk root.

<a id="notesmgr.main_window.MainWindow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(window: Union[tkinter.Tk, tkinter.Toplevel]) -> None
```

Fill the given toplevel window with the notesmgr main window.

<a id="notesmgr.main_window.MainWindow._menu_specs"></a>

#### \_menu\_specs

```python
def _menu_specs(shortcut: Shortcut) -> list[MenuSpec]
```

Return the menus of the main window and what they hold.

The entries that act on a note need a note to act on, the
entries that act on a folder need a folder, and copying the
configuration to the user wide location asks for a project
configuration file to copy, so all of them are greyed out
until what they need is selected.

<a id="notesmgr.main_window.MainWindow._note_entries"></a>

#### \_note\_entries

```python
def _note_entries() -> list[MenuEntry]
```

Return one entry of the note menu for every working button.

The note menu and the button row do the same things, so they
are described in one place, which is the panel that holds the
buttons. A button whose operation belongs to a later step of
the plan has nothing to do yet, and is left out of the menu
until it has.

<a id="notesmgr.main_window.MainWindow._folder_entries"></a>

#### \_folder\_entries

```python
def _folder_entries() -> list[MenuEntry]
```

Return the entries that act on a folder of the project.

<a id="notesmgr.main_window.MainWindow._bind_quit_shortcut"></a>

#### \_bind\_quit\_shortcut

```python
def _bind_quit_shortcut(shortcut: Shortcut) -> None
```

Let the shortcut shown on the Quit entry close the window.

Tk installs no binding for a menu accelerator, so the key
sequence has to be bound as well. It is bound on this window
only, so that it cannot close the main window from a dialog
that happens to have the keyboard focus.

<a id="notesmgr.main_window.MainWindow._shape_window"></a>

#### \_shape\_window

```python
def _shape_window() -> None
```

Lay out the panes and give the window its size.

<a id="notesmgr.main_window.MainWindow.show_project"></a>

#### show\_project

```python
def show_project(project_name: Optional[str]) -> None
```

Name the open project in the window title, None meaning none.

<a id="notesmgr.main_window.MainWindow.show_selected"></a>

#### show\_selected

```python
def show_selected(path: Optional[Path]) -> None
```

Show what the explorer has selected in the note panel.

<a id="notesmgr.main_window.MainWindow.offer_actions"></a>

#### offer\_actions

```python
def offer_actions(labels: AbstractSet[str]) -> None
```

Offer what can be done now, and grey out what cannot.

The buttons of the panel and the entries of the note and
folder menus do the same things, so they are offered and
taken back together, whenever another item is selected and
whenever the note that is shown is taken away.

**Arguments**:

- `labels` - What the actions that can be done now are called.

<a id="notesmgr.main_window.MainWindow.new_project_dialog"></a>

#### new\_project\_dialog

```python
def new_project_dialog() -> None
```

Ask for a folder and make a notesmgr project of it.

A folder that is a project already is not made into one twice,
and opening it is what the user is offered instead.

<a id="notesmgr.main_window.MainWindow.open_project_dialog"></a>

#### open\_project\_dialog

```python
def open_project_dialog() -> None
```

Ask for a project folder and open the project in it.

<a id="notesmgr.main_window.MainWindow.load_project"></a>

#### load\_project

```python
def load_project(root: Path, selected: Optional[Path] = None) -> None
```

Open an existing project and show what it holds.

**Arguments**:

- `root` - The root folder of the project to open.
- `selected` - What to select in it, None for nothing at all.

<a id="notesmgr.main_window.MainWindow.make_project"></a>

#### make\_project

```python
def make_project(root: Path) -> None
```

Make a folder into a project, then open it and show it.

<a id="notesmgr.main_window.MainWindow.reopen"></a>

#### reopen

```python
def reopen(selected: Optional[Path]) -> None
```

Show the open project again, selecting one item of it.

Every command changes the files of the project, so the whole
project is read again rather than the tree being mended item
by item. That way the tree says what the folders really hold,
whatever another program did to them meanwhile.

**Arguments**:

- `selected` - What to select once it is shown again, None to
  select nothing at all.

<a id="notesmgr.main_window.MainWindow.opened"></a>

#### opened

```python
def opened(opening: Callable[[], OpenReport],
           selected: Optional[Path] = None) -> None
```

Show what an opening gave, or say why it gave nothing.

<a id="notesmgr.main_window.MainWindow.choose_template"></a>

#### choose\_template

```python
def choose_template(folder: Path, templates: Sequence[Path]) -> Optional[Path]
```

Ask which of the templates of a folder is the one to keep.

**Arguments**:

- `folder` - The folder that holds more than one template.
- `templates` - The templates that it holds.
  

**Returns**:

  The template to keep, None when the user chose none.

<a id="notesmgr.main_window.MainWindow.show_opened"></a>

#### show\_opened

```python
def show_opened(report: OpenReport, selected: Optional[Path]) -> None
```

Show a project that was opened, and what opening it did.

<a id="notesmgr.main_window.MainWindow.select"></a>

#### select

```python
def select(path: Optional[Path]) -> None
```

Select one item of the tree, and show what is selected.

Tk tells of a selection it was given only once it comes to
handle its own events, which is too late for a command that
wants to see the project as it now stands, so the panel is
told here rather than waiting for the event.

**Arguments**:

- `path` - What to select, None to select nothing at all.

<a id="notesmgr.main_window.MainWindow.tell_about_opening"></a>

#### tell\_about\_opening

```python
def tell_about_opening(report: OpenReport) -> None
```

Tell what opening a project changed and what it could not do.

<a id="notesmgr.main_window.MainWindow.edit_configuration"></a>

#### edit\_configuration

```python
def edit_configuration() -> None
```

Open the editor of the configuration that is in use.

That is the configuration of the open project, and the user
wide configuration while no project is open. One session at a
time is enough, and the editor holds the application while it
is open, so a second one is not started.

<a id="notesmgr.main_window.MainWindow._config_closed"></a>

#### \_config\_closed

```python
def _config_closed() -> None
```

Take up again what the configuration editor may have changed.

The configuration says what the notes and the templates of a
project are called, so an open project is opened once more
when an editing session has ended.

<a id="notesmgr.main_window.MainWindow.save_user_wide"></a>

#### save\_user\_wide

```python
def save_user_wide() -> None
```

Copy the project's configuration to the user wide file.

<a id="notesmgr.main_window.MainWindow.show_version"></a>

#### show\_version

```python
def show_version() -> None
```

Show what notesmgr and the packages below it are.

Gathering the report asks PyPI whether there are newer
releases, which takes a moment, so the window says that it is
working while that is going on.

<a id="notesmgr.main_window.MainWindow.quit"></a>

#### quit

```python
def quit() -> None
```

Destroy the main window, which ends the application.

<a id="notesmgr.version_info"></a>

# notesmgr.version\_info

Version information about notesmgr and what it is built on.

<a id="notesmgr.version_info.MAIN_PACKAGE"></a>

#### MAIN\_PACKAGE

Package to install to get a newer notesmgr.

<a id="notesmgr.version_info.REPORTED_PACKAGES"></a>

#### REPORTED\_PACKAGES

Packages whose versions are worth reporting to a user.

<a id="notesmgr.version_info.RECOMMENDED_PYTHON"></a>

#### RECOMMENDED\_PYTHON

Python version that notesmgr is developed and recommended on.

<a id="notesmgr.version_info.SUPPORT_EXPIRES"></a>

#### SUPPORT\_EXPIRES

When notesmgr stops supporting a Python version.

A Python version is supported for about two and a half years after the
next Python version was released, and support always ends on the first
of March. Newer language features are then available sooner than
following the end of life of Python itself would allow.

<a id="notesmgr.version_info.NotesmgrVersions"></a>

## NotesmgrVersions Objects

```python
class NotesmgrVersions(VersionReporter)
```

Report what notesmgr and the packages below it are.

<a id="notesmgr.version_info.NotesmgrVersions.package_names"></a>

#### package\_names

```python
def package_names() -> list[str]
```

Return the packages whose versions are reported.

<a id="notesmgr.version_info.NotesmgrVersions.get_app_support_expires"></a>

#### get\_app\_support\_expires

```python
def get_app_support_expires() -> SupportExpires
```

Return when notesmgr stops supporting an older Python.

<a id="notesmgr.version_info.NotesmgrVersions.get_main_package_name"></a>

#### get\_main\_package\_name

```python
@classmethod
def get_main_package_name(cls) -> str
```

Return the package that an upgrade of notesmgr installs.

<a id="notesmgr.version_info.NotesmgrVersions.recommended_python"></a>

#### recommended\_python

```python
@classmethod
def recommended_python(cls) -> Version
```

Return the Python version that notesmgr recommends.

<a id="notesmgr.version_info.version_report"></a>

#### version\_report

```python
def version_report(out_file: TextIO) -> None
```

Write the version report of notesmgr to the given stream.

The command line gives it the standard output stream, and the
graphical user interface gives it a string that it then shows in a
window, so that both ways of asking report exactly the same thing.

**Arguments**:

- `out_file` - Stream that the report is written to.

<a id="notesmgr.menu_bar"></a>

# notesmgr.menu\_bar

The menu bar of a notesmgr window.

<a id="notesmgr.menu_bar.MenuEntry"></a>

## MenuEntry Objects

```python
class MenuEntry(NamedTuple)
```

One command of a menu, and whether it can be chosen.

<a id="notesmgr.menu_bar.MenuSpec"></a>

## MenuSpec Objects

```python
class MenuSpec(NamedTuple)
```

One menu of a menu bar and the commands it holds.

<a id="notesmgr.menu_bar.MenuBar"></a>

## MenuBar Objects

```python
class MenuBar(NamedTuple)
```

The menu bar widget of a window and its menus by title.

The menus are kept by title so that an entry which only makes
sense in some states can be greyed out and offered again later.

<a id="notesmgr.menu_bar.entry_state"></a>

#### entry\_state

```python
def entry_state(enabled: bool) -> Literal['normal', 'disabled']
```

Return the Tk state of an entry that can or cannot be chosen.

**Arguments**:

- `enabled` - Whether the entry can be chosen.
  

**Returns**:

  The state that Tk knows that by.

<a id="notesmgr.menu_bar.build_menu"></a>

#### build\_menu

```python
def build_menu(menu_bar: tkinter.Menu, spec: MenuSpec) -> tkinter.Menu
```

Create one described menu and add it to a menu bar.

**Arguments**:

- `menu_bar` - The menu bar that the menu is added to.
- `spec` - What the menu is called and what it holds.
  

**Returns**:

  The menu that was made.

<a id="notesmgr.menu_bar.build_menu_bar"></a>

#### build\_menu\_bar

```python
def build_menu_bar(window: Union[tkinter.Tk, tkinter.Toplevel],
                   menus: Sequence[MenuSpec]) -> MenuBar
```

Build the described menus and install them on a window.

An application says what its menus hold and gets them, instead of
calling Tk for every entry of every menu.

**Arguments**:

- `window` - The window that gets the menu bar.
- `menus` - The menus of the menu bar, in the order they are shown.
  

**Returns**:

  The menu bar that was made.

<a id="notesmgr.menu_bar.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(menu: tkinter.Menu, label: str, enabled: bool) -> None
```

Let one entry of a menu be chosen, or grey it out.

**Arguments**:

- `menu` - The menu that the entry is in.
- `label` - Which entry of that menu it is.
- `enabled` - Whether the entry can now be chosen.

<a id="notesmgr.menu_bar.entry_labels"></a>

#### entry\_labels

```python
def entry_labels(menu: tkinter.Menu) -> list[str]
```

Return what the entries of a menu say, in the order they are in.

**Arguments**:

- `menu` - The menu to look through.
  

**Returns**:

  The label of every entry, and nothing at all for a menu that
  holds no entries.

<a id="notesmgr.cmd_line"></a>

# notesmgr.cmd\_line

The command line of the notesmgr application.

<a id="notesmgr.cmd_line.PROGRAM_NAME"></a>

#### PROGRAM\_NAME

Name that the command line help calls this program.

<a id="notesmgr.cmd_line.DESCRIPTION"></a>

#### DESCRIPTION

What the command line help says this program is for.

<a id="notesmgr.cmd_line.FOLDER_HELP"></a>

#### FOLDER\_HELP

What the command line help says about the project folder.

<a id="notesmgr.cmd_line.VERSION_HELP"></a>

#### VERSION\_HELP

What the command line help says about the version flag.

<a id="notesmgr.cmd_line.CommandLine"></a>

## CommandLine Objects

```python
class CommandLine(NamedTuple)
```

What the command line asked notesmgr to do.

<a id="notesmgr.cmd_line.argument_parser"></a>

#### argument\_parser

```python
def argument_parser() -> argparse.ArgumentParser
```

Return the parser that reads the notesmgr command line.

<a id="notesmgr.cmd_line.parse_command_line"></a>

#### parse\_command\_line

```python
def parse_command_line(argv: Optional[list[str]] = None) -> CommandLine
```

Return what the given command line, or sys.argv, asked for.

Whether the named folder holds a project is not decided here. A
graphical application says that in a window of its own, and not on
an error stream that a program started from a desktop has not got.

**Arguments**:

- `argv` - Command line arguments, or None for the ones this
  program was started with.
  

**Returns**:

  What was asked for.

<a id="notesmgr.editor_command"></a>

# notesmgr.editor\_command

Starting the editor that a project is configured with.

<a id="notesmgr.editor_command.PLACEHOLDER"></a>

#### PLACEHOLDER

What the name of the note replaces in the editor command.

<a id="notesmgr.editor_command.ON_WINDOWS"></a>

#### ON\_WINDOWS

Whether a command line is to be read the way Windows reads one.

<a id="notesmgr.editor_command.QUOTES"></a>

#### QUOTES

What a Windows command line may have around one of its words.

<a id="notesmgr.editor_command.UNREADABLE"></a>

#### UNREADABLE

What is said about a command whose quotes do not match.

<a id="notesmgr.editor_command.NO_PROGRAM"></a>

#### NO\_PROGRAM

What is said about a command that holds no word at all.

<a id="notesmgr.editor_command.NOT_STARTED"></a>

#### NOT\_STARTED

What is said about an editor that the system did not start.

<a id="notesmgr.editor_command.unquoted"></a>

#### unquoted

```python
def unquoted(word: str) -> str
```

Return one word of a command line without the quotes around it.

**Arguments**:

- `word` - A word as a Windows command line holds it.
  

**Returns**:

  The word itself, which is what is to be passed on.

<a id="notesmgr.editor_command.split_command"></a>

#### split\_command

```python
def split_command(command: str, windows: bool = ON_WINDOWS) -> list[str]
```

Return the words that an editor command is made of.

A backslash is an escape character to a POSIX shell and a path
separator on Windows, so a Windows command line is split by the
rules that keep its paths whole, and the quotes that splitting
leaves behind are then taken off.

**Arguments**:

- `command` - The editor command as the configuration holds it.
- `windows` - Whether to split it the way Windows does.
  

**Returns**:

  The words of the command, quotes taken off.
  

**Raises**:

- `ValueError` - The quotes of the command do not match.

<a id="notesmgr.editor_command.editor_argv"></a>

#### editor\_argv

```python
def editor_argv(command: str, path: Path) -> list[str]
```

Return the command line that opens one note in the editor.

The name of the note takes the place of every {file} in the
command, and is added at the end of a command that holds none,
so that 'code' and 'code {file}' mean the same thing.

**Arguments**:

- `command` - The editor command as the configuration holds it.
- `path` - The note to open.
  

**Returns**:

  The program to start and the arguments to give it.
  

**Raises**:

- `NotesmgrError` - The command cannot be read, or names nothing
  to start.

<a id="notesmgr.editor_command.start_detached"></a>

#### start\_detached

```python
def start_detached(argv: list[str]) -> None
```

Start a program and leave it running on its own.

The editor outlives the command that started it and is not to be
stopped by what stops notesmgr, so it is put in a session of its
own. Windows knows no sessions and ignores that, which is right
there, where a started program is independent already.

**Arguments**:

- `argv` - The program to start and the arguments to give it.
  

**Raises**:

- `OSError` - The program cannot be started.

<a id="notesmgr.editor_command.launch_editor"></a>

#### launch\_editor

```python
def launch_editor(command: str,
                  path: Path,
                  run: Callable[[list[str]], None] = start_detached) -> None
```

Open one note in the editor that the project is configured with.

**Arguments**:

- `command` - The editor command as the configuration holds it.
- `path` - The note to open.
- `run` - What starts the editor, for a test to stand in for.
  

**Raises**:

- `NotesmgrError` - The command cannot be read, names nothing to
  start, or names a program that the system did not start.

<a id="notesmgr.config"></a>

# notesmgr.config

The configuration of notesmgr and the values it accepts.

<a id="notesmgr.config.EMPTY_EDITOR"></a>

#### EMPTY\_EDITOR

What is said about an editor command that holds no command.

<a id="notesmgr.config.NoteExtension"></a>

## NoteExtension Objects

```python
class NoteExtension(StrEnum)
```

Note file extension: MD is .md, TXT is .txt, MD_TXT is .md.txt.

The configuration file holds the name of one of these members,
while the value of the member is the extension itself. MD_TXT is
the default, because many systems do not recognize .md as a safe
file type.

<a id="notesmgr.config.DEFAULT_EXTENSION"></a>

#### DEFAULT\_EXTENSION

Note file extension that a new configuration starts out with.

<a id="notesmgr.config.DEFAULT_NOTE_SIZE"></a>

#### DEFAULT\_NOTE\_SIZE

Characters of a note that are shown when nothing else is said.

<a id="notesmgr.config.MIN_NOTE_SIZE"></a>

#### MIN\_NOTE\_SIZE

Fewest characters of a note that may be asked to be shown.

A note is meant to be read whole, so a limit small enough to cut a
short note in two is taken for a misunderstanding rather than a wish.

<a id="notesmgr.config.MAX_NOTE_SIZE"></a>

#### MAX\_NOTE\_SIZE

Most characters of a note that may be asked to be shown.

Reading a note is meant to stay quick, and a window that has to draw
far more than this is no longer a notes manager to work in.

<a id="notesmgr.config.OldNotesmgrConfig"></a>

## OldNotesmgrConfig Objects

```python
class OldNotesmgrConfig(ReadOldConfiguration)
```

How a configuration file of an older notesmgr is read.

Every member of the configuration has to be named in the file,
so a file written before a member existed is read with the
built-in default of that member rather than being refused.

<a id="notesmgr.config.OldNotesmgrConfig.get_missing_path_values"></a>

#### get\_missing\_path\_values

```python
def get_missing_path_values() -> dict[ConfigPath, object]
```

Add configuration parameter for things missing in old files.

This is only relevant for configuration parameters that
have been added after the first **released** version of notesmgr.

<a id="notesmgr.config.NotesmgrConfig"></a>

## NotesmgrConfig Objects

```python
class NotesmgrConfig(Config)
```

How notesmgr edits the notes of a project and what it names them.

The editor command is started whenever a note is edited, the
extension is the one that new notes are given and that a file must
have to be a note at all, and the size is how much of a note is
shown before the rest of it is left out.

<a id="notesmgr.config.NotesmgrConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr,
             member_name: Optional[str] = None) -> None
```

Construct the configuration with its default values.

**Arguments**:

- `from_json_data_text` - Optional JSON text to parse directly.
- `from_json_filename` - Optional path to a JSON file to read.
- `stderr_file` - Stream used for user-facing diagnostics.
- `member_name` - Path for reaching this object from the top
  level configuration, None for the top level itself.

<a id="notesmgr.config.NotesmgrConfig._get_read_old_config"></a>

#### \_get\_read\_old\_config

```python
def _get_read_old_config() -> ReadOldConfiguration
```

Return how a file of an older notesmgr is read.

<a id="notesmgr.config.NotesmgrConfig.parse_converters"></a>

#### parse\_converters

```python
def parse_converters() -> dict[str, ParseConverter]
```

Return how the name in the file becomes an extension again.

Declaring it is also what lets the configuration editor offer
the extensions to be chosen instead of to be spelled.

<a id="notesmgr.config.NotesmgrConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return the checks that every configuration has to pass.

<a id="notesmgr.config.NotesmgrConfig.stripped_editor"></a>

#### stripped\_editor

```python
def stripped_editor(value: object) -> str
```

Return the editor command without the blanks around it.

**Arguments**:

- `value` - The editor command as it was read or typed.
  

**Returns**:

  The same command with no leading or trailing blanks.
  

**Raises**:

- `InvalidConfiguration` - Nothing but blanks was given.

<a id="notesmgr.note_ops"></a>

# notesmgr.note\_ops

Making, copying, moving and taking away the notes of a project.

<a id="notesmgr.note_ops.NAME_TAKEN"></a>

#### NAME\_TAKEN

What is said about a name that is another file's name already.

<a id="notesmgr.note_ops.NOT_WRITTEN"></a>

#### NOT\_WRITTEN

What is said about a note that the file system would not take.

<a id="notesmgr.note_ops.NOT_COPIED"></a>

#### NOT\_COPIED

What is said about a note that could not be copied.

<a id="notesmgr.note_ops.NOT_TRASHED"></a>

#### NOT\_TRASHED

What is said about a note that the trash would not take.

<a id="notesmgr.note_ops.resync_order"></a>

#### resync\_order

```python
def resync_order(folder: Path) -> list[str]
```

Return the notes of a folder, bringing its order file in line.

The notes of a folder change under its order file whenever one is
made, copied or taken away, and the repair that opening a project
does is exactly what is wanted then, so it is done here as well.

**Arguments**:

- `folder` - The folder whose notes have changed.
  

**Returns**:

  The notes of the folder, in the order they are shown in.
  

**Raises**:

- `NotesmgrError` - The folder or its order file cannot be read,
  or the order file cannot be written.

<a id="notesmgr.note_ops.free_path"></a>

#### free\_path

```python
def free_path(folder: Path, name: str) -> Path
```

Return the file that a name asks for, refusing a taken name.

Two names that differ only in case are one file on macOS and on
Windows, so a name is taken when the folder holds any name equal
to it but for its case, whatever this file system makes of it.

**Arguments**:

- `folder` - The folder that the file is to be in.
- `name` - The name of the file, extension and all.
  

**Returns**:

  The file to write, which is not there yet.
  

**Raises**:

- `NotesmgrError` - The folder holds a file of that name already,
  or the folder cannot be read.

<a id="notesmgr.note_ops.new_path"></a>

#### new\_path

```python
def new_path(folder: Path, typed: str, extension: NoteExtension) -> Path
```

Return the note file that a typed name asks for in a folder.

**Arguments**:

- `folder` - The folder that the note is to be in.
- `typed` - What the user typed as the name of the note.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The note file to write, which is not there yet.
  

**Raises**:

- `NotesmgrError` - The name names no note of this project, or it
  is the name of a file that is there already.

<a id="notesmgr.note_ops.template_text"></a>

#### template\_text

```python
def template_text(folder: Path, extension: NoteExtension) -> str
```

Return what a new note in a folder starts out holding.

That is the template of the folder, and nothing at all when the
folder holds no template that can be read, which is no reason to
refuse to make the note.

**Arguments**:

- `folder` - The folder that the new note is made in.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The text that the new note starts out holding.

<a id="notesmgr.note_ops.new_note"></a>

#### new\_note

```python
def new_note(folder: Path, typed: str, extension: NoteExtension) -> Path
```

Make a note in a folder, holding what its template holds.

**Arguments**:

- `folder` - The folder that the note is made in.
- `typed` - What the user typed as the name of the note.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The note that was made.
  

**Raises**:

- `NotesmgrError` - The name names no note that can be made here,
  or the note or the note order cannot be written.

<a id="notesmgr.note_ops.duplicate_note"></a>

#### duplicate\_note

```python
def duplicate_note(note: Path, folder: Path, typed: str,
                   extension: NoteExtension) -> Path
```

Copy a note into a folder of the project under another name.

**Arguments**:

- `note` - The note to copy.
- `folder` - The folder that the copy is made in, which is any
  folder of the project and not only the note's own.
- `typed` - What the user typed as the name of the copy.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The copy that was made.
  

**Raises**:

- `NotesmgrError` - The name names no note that can be made here,
  or the copy or the note order cannot be written.

<a id="notesmgr.note_ops.delete_note"></a>

#### delete\_note

```python
def delete_note(note: Path) -> None
```

Move a note to the trash, and out of the order of its folder.

**Arguments**:

- `note` - The note to take away.
  

**Raises**:

- `NotesmgrError` - The trash would not take the note, or the note
  order cannot be written.

<a id="notesmgr.note_ops.moved_order"></a>

#### moved\_order

```python
def moved_order(names: Sequence[str], name: str, offset: int) -> list[str]
```

Return an order with one of its notes moved so many places.

A note at the first place cannot be moved further up and one at
the last place cannot be moved further down, so it stays where it
is rather than moving round the end of the folder.

**Arguments**:

- `names` - The notes of a folder, in the order they are shown in.
- `name` - The note to move, which may be none of them.
- `offset` - How many places to move it, up being negative.
  

**Returns**:

  The order as it is after the move.

<a id="notesmgr.note_ops.move_note"></a>

#### move\_note

```python
def move_note(note: Path, offset: int) -> Path
```

Move a note so many places in the order of its folder.

**Arguments**:

- `note` - The note to move.
- `offset` - How many places to move it, up being negative.
  

**Returns**:

  The note, which is where it now stands in its folder.
  

**Raises**:

- `NotesmgrError` - The folder or its order file cannot be read,
  or the order file cannot be written.

<a id="notesmgr.session"></a>

# notesmgr.session

What one run of the notesmgr application knows.

<a id="notesmgr.session.start_folder"></a>

#### start\_folder

```python
def start_folder() -> Path
```

Return the folder the application was started from.

A folder that has been taken away while the program was starting
is no place to look for notes in, so the home folder stands in
for it rather than letting the program fail to start.

<a id="notesmgr.session.Session"></a>

## Session Objects

```python
class Session()
```

The open project of one run, and where to look for the next one.

notesmgr remembers no project from one run to the next, but within
one run it remembers where the user was last looking: a folder
chooser starts in the project that was opened last, and in the
folder the application was started from until one has been.

<a id="notesmgr.session.Session.__init__"></a>

#### \_\_init\_\_

```python
def __init__(folder: Optional[Path] = None) -> None
```

Begin a session in which no project has been opened yet.

**Arguments**:

- `folder` - Where a folder chooser starts until a project has
  been opened, None for the folder the application was
  started from.

<a id="notesmgr.session.Session.opened"></a>

#### opened

```python
def opened(project: Project) -> None
```

Take a project as the one that is open from now on.

<a id="notesmgr.session.Session.chooser_folder"></a>

#### chooser\_folder

```python
def chooser_folder() -> Path
```

Return the folder that a folder chooser is to start in.

<a id="notesmgr.session.Session.config_file"></a>

#### config\_file

```python
def config_file() -> Optional[Path]
```

Return the configuration file of the open project, if any.

<a id="notesmgr.session.Session.config"></a>

#### config

```python
def config() -> Optional[NotesmgrConfig]
```

Return the configuration in use, None while none is.

It says what the notes of the project are named, how much of
a note is shown and what editor a note is opened in, so it is
what the parts of the window ask when they need any of that.

<a id="notesmgr.actions"></a>

# notesmgr.actions

What can be done with what is selected, and when it can be done.

<a id="notesmgr.actions.COPY_RAW"></a>

#### COPY\_RAW

What the action that copies the note as it is written is called.

<a id="notesmgr.actions.COPY_FORMATTED"></a>

#### COPY\_FORMATTED

What the action that copies the note formatted is called.

<a id="notesmgr.actions.DUPLICATE"></a>

#### DUPLICATE

What the action that copies the note into the project is called.

<a id="notesmgr.actions.EDIT"></a>

#### EDIT

What the action that opens the note in an editor is called.

<a id="notesmgr.actions.NEW"></a>

#### NEW

What the action that makes another note is called.

<a id="notesmgr.actions.DELETE"></a>

#### DELETE

What the action that takes the note away is called.

<a id="notesmgr.actions.MOVE_UP"></a>

#### MOVE\_UP

What the action that moves the note one place up is called.

<a id="notesmgr.actions.MOVE_DOWN"></a>

#### MOVE\_DOWN

What the action that moves the note one place down is called.

<a id="notesmgr.actions.NEW_FOLDER"></a>

#### NEW\_FOLDER

What the action that makes another folder is called.

<a id="notesmgr.actions.RENAME_FOLDER"></a>

#### RENAME\_FOLDER

What the action that gives a folder another name is called.

<a id="notesmgr.actions.DELETE_FOLDER"></a>

#### DELETE\_FOLDER

What the action that takes an empty folder away is called.

<a id="notesmgr.actions.ON_NOTE"></a>

#### ON\_NOTE

What can be done with any note that is shown, template or not.

<a id="notesmgr.actions.ON_PLAIN"></a>

#### ON\_PLAIN

What can be done with a note that is no template of a folder.

<a id="notesmgr.actions.ON_PROJECT"></a>

#### ON\_PROJECT

What can be done as long as there is a project to do it in.

<a id="notesmgr.actions.ON_FOLDER"></a>

#### ON\_FOLDER

What can be done with a folder that is no root of a project.

<a id="notesmgr.actions.Selected"></a>

## Selected Objects

```python
class Selected(NamedTuple)
```

What is selected, as far as it says what can be done with it.

The panel knows whether there is a note to act on, because a note
can be taken away by another program while it is shown, and the
rest follows from the item that the explorer has selected.

<a id="notesmgr.actions.NOTHING"></a>

#### NOTHING

What is selected while nothing at all is.

<a id="notesmgr.actions.offered"></a>

#### offered

```python
def offered(selected: Selected) -> frozenset[str]
```

Return what can be done with what is selected.

**Arguments**:

- `selected` - What the explorer has selected now.
  

**Returns**:

  The actions that the buttons and the menu entries offer,
  every other action of the application being greyed out.

<a id="notesmgr.config_files"></a>

# notesmgr.config\_files

Where the user wide configuration of notesmgr is kept.

<a id="notesmgr.config_files.CONFIG_VARIABLE"></a>

#### CONFIG\_VARIABLE

Environment variable in which a user names the configuration file.

<a id="notesmgr.config_files.CONFIG_NAME"></a>

#### CONFIG\_NAME

Name the user wide configuration has in the home folder.

<a id="notesmgr.config_files.MISSING"></a>

#### MISSING

What is said about a configuration file that is not there.

<a id="notesmgr.config_files.NOT_READ"></a>

#### NOT\_READ

What is said about a configuration file that cannot be read.

<a id="notesmgr.config_files.NOT_WRITTEN"></a>

#### NOT\_WRITTEN

What is said about a configuration file that cannot be written.

<a id="notesmgr.config_files.user_config_path"></a>

#### user\_config\_path

```python
def user_config_path() -> Path
```

Return the file the user wide configuration is written to.

The file the environment names is the one the user has asked for,
whether it is there yet or not, so that it is also where a first
configuration is written.

<a id="notesmgr.config_files.user_config_source"></a>

#### user\_config\_source

```python
def user_config_source() -> Optional[Path]
```

Return the user wide configuration file to read, None for none.

The file the environment names is read when it is there, and the
file in the home folder when it is not, so that a variable naming
a file that does not exist yet leaves the defaults to be used
rather than making the program refuse to start.

<a id="notesmgr.config_files.copy_to_user_wide"></a>

#### copy\_to\_user\_wide

```python
def copy_to_user_wide(source: Path) -> Path
```

Copy a project's configuration file to the user wide location.

**Arguments**:

- `source` - The project configuration file to copy.
  

**Returns**:

  The user wide configuration file that was written.
  

**Raises**:

- `OSError` - The file could not be read or could not be written.

<a id="notesmgr.config_files.config_error"></a>

#### config\_error

```python
def config_error(template: str, path: Path, said: str,
                 error: Exception) -> NotesmgrError
```

Return what to raise when a configuration file cannot be used.

What the configuration library said while it was failing tells the
user far more than the exception does, so it is what is shown when
there is any, and the exception is what is shown when there is not.

**Arguments**:

- `template` - What is said about the file, holding path and reason.
- `path` - The configuration file that could not be used.
- `said` - What the configuration library reported while failing.
- `error` - What the configuration library raised.
  

**Returns**:

  The error to raise, said in words meant for the user.

<a id="notesmgr.config_files.read_config_file"></a>

#### read\_config\_file

```python
def read_config_file(path: Path) -> NotesmgrConfig
```

Return the configuration that a file holds.

**Arguments**:

- `path` - The configuration file to read.
  

**Returns**:

  The configuration it holds.
  

**Raises**:

- `NotesmgrError` - There is no such file, or it holds no
  configuration that notesmgr can use.

<a id="notesmgr.config_files.write_config_file"></a>

#### write\_config\_file

```python
def write_config_file(config: NotesmgrConfig, path: Path) -> None
```

Write a configuration to a file, replacing what was there.

**Arguments**:

- `config` - The configuration to write.
- `path` - The configuration file to write it to.
  

**Raises**:

- `NotesmgrError` - The file cannot be written.

<a id="notesmgr.config_files.user_wide_config"></a>

#### user\_wide\_config

```python
def user_wide_config() -> NotesmgrConfig
```

Return the user wide configuration, or the built-in defaults.

**Returns**:

  What a new project starts its own configuration out as.
  

**Raises**:

- `NotesmgrError` - There is a user wide configuration file and it
  holds no configuration that notesmgr can use.

<a id="notesmgr.button_row"></a>

# notesmgr.button\_row

The row of buttons above the note, and how it is made to fit.

<a id="notesmgr.button_row.GAP"></a>

#### GAP

Pixels left between two buttons that stand side by side.

<a id="notesmgr.button_row.ButtonSpec"></a>

## ButtonSpec Objects

```python
class ButtonSpec(NamedTuple)
```

One button of the row, and what pressing it does.

A button whose operation belongs to a later step of the plan has
no command, and is greyed out whatever is selected, so that the
row is the whole row from the start.

<a id="notesmgr.button_row.grid_width"></a>

#### grid\_width

```python
def grid_width(widths: Sequence[int], columns: int, gap: int) -> int
```

Return how wide a grid of buttons of these widths is.

The buttons are placed row by row, so the buttons of one column
are every columns-th of them, and a column is as wide as the
widest button standing in it.

**Arguments**:

- `widths` - How wide each button is, in the order they are shown.
- `columns` - How many buttons stand side by side.
- `gap` - Pixels left beside each button.
  

**Returns**:

  The width the grid needs, and nothing for no buttons at all.

<a id="notesmgr.button_row.fitting_columns"></a>

#### fitting\_columns

```python
def fitting_columns(widths: Sequence[int], available: int, gap: int) -> int
```

Return how many buttons to put side by side in a given width.

The buttons are spread over the fewest rows that fit, so that a
wide panel shows one row and a narrow one shows several rows of
about the same length rather than one long row and a short one.
A width too small for even one button still gives one column,
because a button cut off at the edge is better than none at all.

**Arguments**:

- `widths` - How wide each button is, in the order they are shown.
- `available` - Pixels the row has to lay the buttons out in.
- `gap` - Pixels left beside each button.
  

**Returns**:

  How many buttons stand side by side, at least one.

<a id="notesmgr.button_row.ButtonRow"></a>

## ButtonRow Objects

```python
class ButtonRow()
```

The buttons above the note, in as few rows as the width allows.

A button is as wide as its text and the theme of the platform
make it, and the panel is as wide as the user makes the window,
so the buttons are laid out again whenever the width changes.
That way none of them is ever cut off at the edge of the panel,
at any size the window can be given.

<a id="notesmgr.button_row.ButtonRow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc, specs: Sequence[ButtonSpec]) -> None
```

Build the described buttons in a frame of their own.

**Arguments**:

- `parent` - The widget that the row is placed in.
- `specs` - The buttons, in the order they are shown.

<a id="notesmgr.button_row.ButtonRow._built"></a>

#### \_built

```python
def _built(spec: ButtonSpec) -> ttk.Button
```

Return one button of the row, greyed out to start with.

<a id="notesmgr.button_row.ButtonRow._width_changed"></a>

#### \_width\_changed

```python
def _width_changed(event: 'tkinter.Event[ttk.Frame]') -> None
```

Lay the buttons out again when the row has another width.

<a id="notesmgr.button_row.ButtonRow.widths"></a>

#### widths

```python
def widths() -> list[int]
```

Return how wide each button of the row asks to be.

<a id="notesmgr.button_row.ButtonRow.fit_into"></a>

#### fit\_into

```python
def fit_into(available: int) -> None
```

Lay the buttons out for a row of the given width.

Laying out a grid that is already laid out that way would
make Tk report another width and ask again, so it is only
done when another number of buttons fits now.

**Arguments**:

- `available` - Pixels the row has to lay the buttons out in.

<a id="notesmgr.button_row.ButtonRow.lay_out"></a>

#### lay\_out

```python
def lay_out(columns: int) -> None
```

Put the buttons into a grid so many buttons wide.

<a id="notesmgr.button_row.ButtonRow.offer"></a>

#### offer

```python
def offer(labels: AbstractSet[str]) -> None
```

Let the buttons that can be used now be pressed.

A button whose operation belongs to a later step of the plan
has nothing to do when pressed, and stays greyed out however
much the selection would allow it.

**Arguments**:

- `labels` - What the buttons that can be used now say.

<a id="notesmgr.config_editor"></a>

# notesmgr.config\_editor

Opening the editor of the notesmgr configuration.

<a id="notesmgr.config_editor.editor_files"></a>

#### editor\_files

```python
def editor_files(config_file: Optional[Path]) -> tuple[Optional[Path], Path]
```

Return the files that the configuration editor reads and writes.

The configuration of a project is read and written in the one
place it lives. The user wide configuration is read where there is
one and started from the built-in defaults where there is not,
while it is written to the file the user asked for either way.

**Arguments**:

- `config_file` - The configuration file of the open project, None
  when no project is open.
  

**Returns**:

  The file to read, None for the built-in defaults, and the file
  to write.

<a id="notesmgr.config_editor.open_config_editor"></a>

#### open\_config\_editor

```python
def open_config_editor(parent: tkinter.Misc,
                       on_close: Callable[[], None],
                       config_file: Optional[Path] = None) -> TkEditorPanel
```

Open an editor of the configuration in use, over a window.

The application owns a Tk main loop already, and a second one
would be a second Tcl interpreter that no widget of the first can
reach, so the editor is a panel over the main window rather than
one of the entry points that own a main loop themselves. It
returns at once, and on_close says that the session has ended.

**Arguments**:

- `parent` - The window that the editor is shown over.
- `on_close` - Told when the editing session has ended.
- `config_file` - The configuration file of the open project, None
  for editing the user wide configuration.
  

**Returns**:

  The panel of the session that was started.
  

**Raises**:

- `ConfigLoadError` - The configuration file cannot be edited.

<a id="notesmgr.application"></a>

# notesmgr.application

Start-up of the notesmgr application.

<a id="notesmgr.application.main"></a>

#### main

```python
def main(argv: Optional[list[str]] = None) -> None
```

Run the notesmgr graphical user interface until the user quits.

A command line asking for version information is answered on the
standard output stream, and no window is opened for it. A command
line naming a project folder opens that project, and says in a
window of its own when the folder holds no project.

**Arguments**:

- `argv` - Command line arguments, or None for the ones this
  program was started with.

<a id="notesmgr.trash"></a>

# notesmgr.trash

Moving what notesmgr takes away to the trash of the system.

<a id="notesmgr.trash.send_to_trash"></a>

#### send\_to\_trash

```python
def send_to_trash(path: Path, message: str) -> None
```

Move a file or a folder to the trash of the operating system.

Nothing that notesmgr takes away is deleted outright, so that
anything taken away by mistake can be taken back out of the
trash again.

**Arguments**:

- `path` - The file or folder that is to be moved to the trash.
- `message` - What to tell the user when it cannot be, holding a
  {path} and a {reason} to be filled in.
  

**Raises**:

- `NotesmgrError` - The trash did not take it.

<a id="notesmgr.config_defaults"></a>

# notesmgr.config\_defaults

The values a notesmgr configuration starts out with.

<a id="notesmgr.config_defaults.VISUAL_CODE"></a>

#### VISUAL\_CODE

Command that starts Microsoft Visual Studio Code.

<a id="notesmgr.config_defaults.VISUAL_CODE_FLAG"></a>

#### VISUAL\_CODE\_FLAG

Flag to open a new window in Microsoft Visual Studio Code.

<a id="notesmgr.config_defaults.EDITOR_VARIABLE"></a>

#### EDITOR\_VARIABLE

Environment variable in which a user names a preferred editor.

<a id="notesmgr.config_defaults.PLATFORM_EDITORS"></a>

#### PLATFORM\_EDITORS

Editor command of the platforms that are known to have one.

<a id="notesmgr.config_defaults.OTHER_EDITOR"></a>

#### OTHER\_EDITOR

Editor command used on a platform that is not known here.

<a id="notesmgr.config_defaults.default_editor"></a>

#### default\_editor

```python
def default_editor() -> str
```

Return the editor command a new configuration starts out with.

Microsoft Visual Studio Code is taken when it is installed, then
the editor the user has named in the environment, and after that
whatever the running platform is known to have. A variable that
holds nothing but blanks names no editor and is passed over.

The command carries no arguments, because the name of the note
file is appended to a command that does not place it itself.

<a id="notesmgr.note_panel"></a>

# notesmgr.note\_panel

The panel at the right of the main window, showing a note.

<a id="notesmgr.note_panel.PADDING"></a>

#### PADDING

Space in pixels left around what the panel shows.

<a id="notesmgr.note_panel.NotePanel"></a>

## NotePanel Objects

```python
class NotePanel()
```

Shows the selected note and the buttons that act upon it.

The note that the buttons act on is the file that the watch is
following, so that one place says what the panel is showing. It
is the selected file when that is a note or the template of a
folder, and nothing when a folder or nothing at all is selected.

<a id="notesmgr.note_panel.NotePanel.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc, session: Session,
             commands: Commands) -> None
```

Build the panel in a frame of its own inside a parent widget.

**Arguments**:

- `parent` - The widget that the panel is placed in.
- `session` - What the run knows, which is the open project and
  therefore the editor and the size that are configured.
- `commands` - What the buttons of the panel do when pressed,
  which is also what is told what is selected now.

<a id="notesmgr.note_panel.NotePanel._button_specs"></a>

#### \_button\_specs

```python
def _button_specs() -> list[ButtonSpec]
```

Return the buttons of the row in the order they are shown.

<a id="notesmgr.note_panel.NotePanel.actions"></a>

#### actions

```python
def actions() -> Sequence[ButtonSpec]
```

Return what the buttons of the panel are and what they do.

<a id="notesmgr.note_panel.NotePanel.note_limit"></a>

#### note\_limit

```python
def note_limit() -> int
```

Return how much of a note the open project shows.

With no project open there is no note to show either, so the
built-in default stands in for a configuration that is not
there rather than making the panel a special case.

<a id="notesmgr.note_panel.NotePanel.note_path"></a>

#### note\_path

```python
def note_path() -> Optional[Path]
```

Return the note the panel is showing, None when it shows none.

<a id="notesmgr.note_panel.NotePanel.has_note"></a>

#### has\_note

```python
def has_note() -> bool
```

Return whether there is a note for the buttons to act on.

<a id="notesmgr.note_panel.NotePanel.show_path"></a>

#### show\_path

```python
def show_path(path: Optional[Path]) -> None
```

Show what the explorer has selected.

**Arguments**:

- `path` - What is selected in the explorer, None for nothing.
  A folder is shown by its path alone, and a note and
  the template of a folder are also read and shown.

<a id="notesmgr.note_panel.NotePanel.reload"></a>

#### reload

```python
def reload() -> None
```

Show what the note that is being watched holds now.

This is what the watch calls when the note has been edited,
written or taken away by another program, so a note that is
gone leaves the panel saying so and the buttons greyed out.

<a id="notesmgr.note_panel.NotePanel.offer"></a>

#### offer

```python
def offer(labels: AbstractSet[str]) -> None
```

Let the buttons that can be used now be pressed.

**Arguments**:

- `labels` - What the actions that can be done now are called.

<a id="notesmgr.note_panel.NotePanel.shown_path"></a>

#### shown\_path

```python
def shown_path() -> str
```

Return the path the panel is showing, empty for none.

<a id="notesmgr.note_panel.NotePanel.edit_note"></a>

#### edit\_note

```python
def edit_note() -> None
```

Open the note that is shown in the editor of the project.

<a id="notesmgr.note_panel.NotePanel.copy_raw"></a>

#### copy\_raw

```python
def copy_raw() -> None
```

Put the text of the note that is shown on the clipboard.

A note that could not be read at all holds no text to copy,
so what is wrong with it is reported rather than the
clipboard being emptied. A note that is shown only in part is
copied as far as it is shown, which is what the warning above
it says.

<a id="notesmgr.project_ops"></a>

# notesmgr.project\_ops

Opening a folder of notes as a notesmgr project.

<a id="notesmgr.project_ops.ALREADY_PROJECT"></a>

#### ALREADY\_PROJECT

What is said about a folder that is not to be made a project twice.

<a id="notesmgr.project_ops.UNRESOLVED"></a>

#### UNRESOLVED

What is said when the user did not say which template to keep.

<a id="notesmgr.project_ops.NOT_TRASHED"></a>

#### NOT\_TRASHED

What is said about a template too many that cannot be trashed.

<a id="notesmgr.project_ops.NOT_RENAMED"></a>

#### NOT\_RENAMED

What is said about a template that cannot be given the right name.

<a id="notesmgr.project_ops.NOT_CREATED"></a>

#### NOT\_CREATED

What is said about a template that a folder lacks and cannot get.

<a id="notesmgr.project_ops.RENAMED_HEAD"></a>

#### RENAMED\_HEAD

Heading over the templates that opening the project renamed.

<a id="notesmgr.project_ops.CREATED_HEAD"></a>

#### CREATED\_HEAD

Heading over the templates that opening the project created.

<a id="notesmgr.project_ops.OpenReport"></a>

## OpenReport Objects

```python
class OpenReport(NamedTuple)
```

An opened project, and what opening it did to the files.

Opening a project repairs what it finds, so the user is told what
was changed and what could not be done, rather than finding it out
later from the file system.

<a id="notesmgr.project_ops.ProjectOpener"></a>

## ProjectOpener Objects

```python
class ProjectOpener()
```

Reads a project folder, repairing what it finds on the way.

Every folder of a project holds one template carrying the file
extension of the project, and a note order file listing the notes
that are really there. This makes that true as the tree is read.

Which of several templates in one folder is the one to keep is the
only question with no right answer, so a chooser is asked, and an
answer of None refuses to open the project at all. Everything else
that cannot be done is gathered as a problem to be reported, and
the rest of the project is still opened.

<a id="notesmgr.project_ops.ProjectOpener.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
        root: Path, config: NotesmgrConfig,
        chooser: Callable[[Path, Sequence[Path]], Optional[Path]]) -> None
```

Get ready to read the project in a folder.

**Arguments**:

- `root` - The root folder of the project.
- `config` - The configuration that the project is used with.
- `chooser` - Asked which of the templates of a folder is the
  one to keep, whenever a folder holds more than one.

<a id="notesmgr.project_ops.ProjectOpener.read"></a>

#### read

```python
def read() -> OpenReport
```

Return the project, having repaired what needed repair.

**Raises**:

- `NotesmgrError` - A folder holds several templates, and the
  user did not say which of them to keep.

<a id="notesmgr.project_ops.ProjectOpener.folder"></a>

#### folder

```python
def folder(folder: Path, parent: Optional[Path]) -> Folder
```

Return one folder of the tree, and everything below it.

**Arguments**:

- `folder` - The folder to read.
- `parent` - Template of the folder above, None in the root.
  

**Returns**:

  The folder as it is shown, and empty when it cannot be
  read at all, which is reported as a problem instead.

<a id="notesmgr.project_ops.ProjectOpener.repaired"></a>

#### repaired

```python
def repaired(folder: Path, content: FolderContent,
             parent: Optional[Path]) -> Folder
```

Return a folder whose template and note order are in order.

<a id="notesmgr.project_ops.ProjectOpener.notes"></a>

#### notes

```python
def notes(folder: Path, names: Sequence[str]) -> list[Path]
```

Return the notes of a folder in the order they are shown in.

A note order file that cannot be read or written is reported,
and its folder is then shown in alphabetical order instead.

<a id="notesmgr.project_ops.ProjectOpener.template"></a>

#### template

```python
def template(folder: Path, templates: Sequence[Path],
             parent: Optional[Path]) -> Optional[Path]
```

Return the one template of a folder, making it the only one.

**Arguments**:

- `folder` - The folder the template belongs to.
- `templates` - The templates that the folder holds now.
- `parent` - Template of the folder above, None in the root.
  

**Returns**:

  The template of the folder, None when it has none and
  none could be written.
  

**Raises**:

- `NotesmgrError` - The folder holds several templates, and the
  user did not say which of them to keep.

<a id="notesmgr.project_ops.ProjectOpener.kept_template"></a>

#### kept\_template

```python
def kept_template(folder: Path, templates: Sequence[Path]) -> Optional[Path]
```

Return the template to keep, trashing the ones too many.

**Raises**:

- `NotesmgrError` - There are several templates, and the user
  did not say which of them to keep.

<a id="notesmgr.project_ops.ProjectOpener.trash_template"></a>

#### trash\_template

```python
def trash_template(path: Path) -> None
```

Move a template that is one too many to the trash.

<a id="notesmgr.project_ops.ProjectOpener.rightly_named"></a>

#### rightly\_named

```python
def rightly_named(kept: Path) -> Path
```

Return the template, named with the extension of the project.

**Arguments**:

- `kept` - The template of the folder as it is named now.
  

**Returns**:

  The template under the name it is to have, and under the
  name it had when it could not be renamed.

<a id="notesmgr.project_ops.ProjectOpener.new_template"></a>

#### new\_template

```python
def new_template(folder: Path, parent: Optional[Path]) -> Optional[Path]
```

Return a template written in a folder that held none.

The root folder of a project gets an empty template, and a
folder below it gets a copy of the template of the folder
above it, so that a new folder starts out as its parent does.

**Arguments**:

- `folder` - The folder that is to get a template.
- `parent` - Template of the folder above, None in the root.
  

**Returns**:

  The template that was written, None when it could not be,
  which is reported as a problem instead.

<a id="notesmgr.project_ops.open_project"></a>

#### open\_project

```python
def open_project(
        root: Path, chooser: Callable[[Path, Sequence[Path]],
                                      Optional[Path]]) -> OpenReport
```

Open the project in a folder, repairing what needs repair.

**Arguments**:

- `root` - The root folder of the project.
- `chooser` - Asked which of the templates of a folder is the one
  to keep, whenever a folder holds more than one.
  

**Returns**:

  The project, and what opening it changed on the way.
  

**Raises**:

- `NotesmgrError` - The folder is no project, its configuration
  cannot be used, or a template was not chosen.

<a id="notesmgr.project_ops.create_project"></a>

#### create\_project

```python
def create_project(
        root: Path, chooser: Callable[[Path, Sequence[Path]],
                                      Optional[Path]]) -> OpenReport
```

Make a folder into a project, and open it.

The notes that the folder holds already become the notes of the
project, in alphabetical order, and the configuration of the
project starts out as a copy of the user wide configuration.

**Arguments**:

- `root` - The folder to make into a project.
- `chooser` - Asked which of the templates of a folder is the one
  to keep, whenever a folder holds more than one.
  

**Returns**:

  The project, and what making it wrote on the way.
  

**Raises**:

- `NotesmgrError` - The folder is a project already, or its
  configuration file cannot be written.

<a id="notesmgr.project_ops.named_list"></a>

#### named\_list

```python
def named_list(head: str, paths: Sequence[Path]) -> str
```

Return a heading with the paths below it, nothing for no paths.

<a id="notesmgr.project_ops.changed_message"></a>

#### changed\_message

```python
def changed_message(report: OpenReport) -> str
```

Return what to tell the user that opening a project changed.

**Arguments**:

- `report` - What opening the project gave.
  

**Returns**:

  What to tell, and nothing at all when nothing was changed.

<a id="notesmgr.order_file"></a>

# notesmgr.order\_file

The file that keeps the notes of a folder in their order.

<a id="notesmgr.order_file.ORDER_NAME"></a>

#### ORDER\_NAME

Name of the hidden file that orders the notes of a folder.

<a id="notesmgr.order_file.WRITING_NAME"></a>

#### WRITING\_NAME

Name a new note order is written under until it is whole.

<a id="notesmgr.order_file.NOT_READ"></a>

#### NOT\_READ

What is said about a note order file that cannot be read.

<a id="notesmgr.order_file.NOT_WRITTEN"></a>

#### NOT\_WRITTEN

What is said about a note order file that cannot be written.

<a id="notesmgr.order_file.order_path"></a>

#### order\_path

```python
def order_path(folder: Path) -> Path
```

Return the file that holds the note order of a folder.

<a id="notesmgr.order_file.read_order_text"></a>

#### read\_order\_text

```python
def read_order_text(folder: Path) -> Optional[str]
```

Return the note order file of a folder, None when it has none.

**Arguments**:

- `folder` - Folder of a project.
  

**Returns**:

  The text of the order file, None when there is no order file.
  

**Raises**:

- `NotesmgrError` - There is an order file, and it cannot be read.

<a id="notesmgr.order_file.names_a_file"></a>

#### names\_a\_file

```python
def names_a_file(name: str) -> bool
```

Return whether a line of an order file can name a file at all.

<a id="notesmgr.order_file.parse_order"></a>

#### parse\_order

```python
def parse_order(text: str) -> list[str]
```

Return the file names that a note order file holds, in its order.

The file is written by hand as often as by notesmgr, so a byte
order mark, line endings of any kind, blank lines, blanks around a
name and a name given twice are all taken for what they meant.
A line that can name no file in the folder is left out.

**Arguments**:

- `text` - The text of the order file.
  

**Returns**:

  The names it holds, each of them once.

<a id="notesmgr.order_file.repair_order"></a>

#### repair\_order

```python
def repair_order(listed: Sequence[str], existing: Sequence[str]) -> list[str]
```

Return the order in which the notes of a folder are shown.

Notes that are gone are dropped, and notes that the order file
does not mention are added at the end in alphabetical order, so
that what another program did to the folder is taken up rather
than making the order file worth nothing.

**Arguments**:

- `listed` - The names that the order file holds, in its order.
- `existing` - The names of the notes really in the folder.
  

**Returns**:

  Every existing note once, in the order it is shown in.

<a id="notesmgr.order_file.order_text"></a>

#### order\_text

```python
def order_text(names: Sequence[str]) -> str
```

Return what a note order file holding these names looks like.

<a id="notesmgr.order_file.write_order"></a>

#### write\_order

```python
def write_order(folder: Path, text: str) -> None
```

Write the note order file of a folder, replacing the old one.

The text is written to a file of its own and put in the place of
the order file only once it is whole, so that a program that stops
in the middle leaves the old order rather than half of a new one.

**Arguments**:

- `folder` - Folder of a project.
- `text` - What the order file is to hold.
  

**Raises**:

- `NotesmgrError` - The order file cannot be written.

<a id="notesmgr.order_file.repair_order_file"></a>

#### repair\_order\_file

```python
def repair_order_file(folder: Path, existing: Sequence[str]) -> list[str]
```

Return the note order of a folder, repairing what needs repair.

The file is written only when the repair changed something, so
that opening a project leaves the folders that were in order as
untouched as it found them.

**Arguments**:

- `folder` - Folder of a project.
- `existing` - The names of the notes really in the folder.
  

**Returns**:

  Every existing note once, in the order it is shown in.
  

**Raises**:

- `NotesmgrError` - The order file cannot be read or written.

<a id="notesmgr.explorer_tree"></a>

# notesmgr.explorer\_tree

The tree of a project, shown at the left of the main window.

<a id="notesmgr.explorer_tree.EXPLORER_WIDTH"></a>

#### EXPLORER\_WIDTH

Width in pixels that the explorer asks the main window for.

<a id="notesmgr.explorer_tree.SELECT_EVENT"></a>

#### SELECT\_EVENT

Tk event saying that another item of the tree is selected now.

<a id="notesmgr.explorer_tree.ExplorerTree"></a>

## ExplorerTree Objects

```python
class ExplorerTree()
```

Shows the folders, templates and notes of a project as a tree.

Every item of the tree is known by the path of the file or folder
it stands for, so that what the user selected is a path, and the
view keeps nothing of its own beside the tree itself.

<a id="notesmgr.explorer_tree.ExplorerTree.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc, on_select: Callable[[Optional[Path]],
                                                       None]) -> None
```

Build the tree in a frame of its own inside a parent widget.

**Arguments**:

- `parent` - The widget that the explorer is placed in.
- `on_select` - Told which item is selected, whenever that
  changes, and told None when nothing is selected.

<a id="notesmgr.explorer_tree.ExplorerTree.selection_changed"></a>

#### selection\_changed

```python
def selection_changed(_event: 'tkinter.Event[ttk.Treeview]') -> None
```

Tell whoever is listening what is selected now.

<a id="notesmgr.explorer_tree.ExplorerTree.selected_path"></a>

#### selected\_path

```python
def selected_path() -> Optional[Path]
```

Return what the user selected, None when nothing is.

<a id="notesmgr.explorer_tree.ExplorerTree.select"></a>

#### select

```python
def select(path: Optional[Path]) -> Optional[Path]
```

Select one item of the tree, or nothing at all.

**Arguments**:

- `path` - What is to be selected, None for nothing at all.
  A path that the tree does not show selects nothing
  either, which is what a note that was taken away or
  renamed by another program leaves behind.
  

**Returns**:

  What is selected now, None when nothing is.

<a id="notesmgr.explorer_tree.ExplorerTree.show"></a>

#### show

```python
def show(project: Optional[Project]) -> None
```

Show a project, or nothing at all when there is none.

<a id="notesmgr.explorer_tree.ExplorerTree.add_folder"></a>

#### add\_folder

```python
def add_folder(folder: Folder, parent: str) -> None
```

Add one folder of the project and everything below it.

The subfolders come first, then the template of the folder,
and after them the notes in the order the note order file
gives them.

**Arguments**:

- `folder` - The folder of the project to add.
- `parent` - Item the folder is added under, empty for the top.

<a id="notesmgr.explorer_tree.ExplorerTree.shown_files"></a>

#### shown\_files

```python
@staticmethod
def shown_files(folder: Folder) -> list[Path]
```

Return the template and the notes of a folder, in that order.

<a id="notesmgr.errors"></a>

# notesmgr.errors

What notesmgr raises when it cannot do what it was asked to do.

<a id="notesmgr.errors.NotesmgrError"></a>

## NotesmgrError Objects

```python
class NotesmgrError(Exception)
```

Something cannot be done, said in words meant for the user.

The message is shown in a window as it stands, so it names the
file or the folder it is about and says what is wrong with it,
rather than saying what the code was doing at the time.

<a id="notesmgr.dialogs"></a>

# notesmgr.dialogs

Windows that notesmgr shows over a window of its own.

<a id="notesmgr.dialogs.MIN_TEXT_WIDTH"></a>

#### MIN\_TEXT\_WIDTH

Narrowest that a window showing a text is made, in characters.

<a id="notesmgr.dialogs.MAX_TEXT_WIDTH"></a>

#### MAX\_TEXT\_WIDTH

Widest that a window showing a text is made, in characters.

<a id="notesmgr.dialogs.MAX_TEXT_HEIGHT"></a>

#### MAX\_TEXT\_HEIGHT

Tallest that a window showing a text is made, in lines.

<a id="notesmgr.dialogs.CLOSE_LABEL"></a>

#### CLOSE\_LABEL

What the button that closes a shown text says.

<a id="notesmgr.dialogs.PADDING"></a>

#### PADDING

Space in pixels left around the button of a shown text.

<a id="notesmgr.dialogs.BUSY_CURSOR"></a>

#### BUSY\_CURSOR

Mouse cursor shown while an answer is being gathered.

<a id="notesmgr.dialogs.CHOOSE_LABEL"></a>

#### CHOOSE\_LABEL

What the button that takes the chosen option says.

<a id="notesmgr.dialogs.CANCEL_LABEL"></a>

#### CANCEL\_LABEL

What the button that answers nothing at all says.

<a id="notesmgr.dialogs.ACCEPT_LABEL"></a>

#### ACCEPT\_LABEL

What the button that takes what was filled in says.

<a id="notesmgr.dialogs.NAME_LABEL"></a>

#### NAME\_LABEL

What the field holding a name is called.

<a id="notesmgr.dialogs.FOLDER_LABEL"></a>

#### FOLDER\_LABEL

What the field holding a folder of the project is called.

<a id="notesmgr.dialogs.ENTRY_WIDTH"></a>

#### ENTRY\_WIDTH

Width in characters of the field that a name is typed into.

<a id="notesmgr.dialogs.text_size"></a>

#### text\_size

```python
def text_size(text: str) -> tuple[int, int]
```

Return the width and height in characters that a text needs.

A window is never made narrower than a short line nor wider or
taller than a screen comfortably holds, so a very long line or a
very long text is scrolled to instead of being shown whole.

**Arguments**:

- `text` - The text that is going to be shown.
  

**Returns**:

  The width in characters and the height in lines.

<a id="notesmgr.dialogs.show_text"></a>

#### show\_text

```python
def show_text(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              text: str) -> tkinter.Toplevel
```

Show a text that cannot be edited, over another window.

**Arguments**:

- `parent` - The window that the new window is shown over.
- `title` - What the new window is called.
- `text` - What the new window shows.
  

**Returns**:

  The window that was made, which its own button destroys.

<a id="notesmgr.dialogs._fill_with_text"></a>

#### \_fill\_with\_text

```python
def _fill_with_text(window: tkinter.Toplevel, text: str) -> None
```

Fill a window with a text, a scroll bar and a close button.

<a id="notesmgr.dialogs.show_error"></a>

#### show\_error

```python
def show_error(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               message: str) -> None
```

Tell the user what went wrong, in a window of its own.

**Arguments**:

- `parent` - The window that the message is shown over.
- `title` - What the message window is called.
- `message` - What went wrong.

<a id="notesmgr.dialogs.busy_cursor"></a>

#### busy\_cursor

```python
@contextmanager
def busy_cursor(window: Union[tkinter.Tk, tkinter.Toplevel]) -> Iterator[None]
```

Show the waiting cursor while something slow is being done.

**Arguments**:

- `window` - The window that is going to be busy.
  

**Yields**:

  Nothing. The cursor is put back when the block has ended,
  whether it ended by finishing or by raising.

<a id="notesmgr.dialogs.ask_folder"></a>

#### ask\_folder

```python
def ask_folder(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               folder: Path) -> Optional[Path]
```

Ask the user for a folder that is there.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `folder` - The folder that the chooser starts in.
  

**Returns**:

  The folder that was chosen, None when none was.

<a id="notesmgr.dialogs.ask_yes_no"></a>

#### ask\_yes\_no

```python
def ask_yes_no(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               question: str) -> bool
```

Ask the user something that is answered with yes or no.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `question` - What the user is asked.
  

**Returns**:

  Whether the user answered yes.

<a id="notesmgr.dialogs.show_info"></a>

#### show\_info

```python
def show_info(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              message: str) -> None
```

Tell the user something that is no cause for worry.

**Arguments**:

- `parent` - The window that the message is shown over.
- `title` - What the message window is called.
- `message` - What the user is told.

<a id="notesmgr.dialogs.AskingWindow"></a>

## AskingWindow Objects

```python
class AskingWindow()
```

A window that asks the user something and waits for an answer.

The window is built by the constructor, and the answer is waited
for by answered(), so that a test can look at the window and
answer it by pressing its buttons without a main loop of its own.

<a id="notesmgr.dialogs.AskingWindow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str) -> None
```

Build the window, which is empty until it is filled in.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.

<a id="notesmgr.dialogs.AskingWindow.ask"></a>

#### ask

```python
def ask(question: str) -> None
```

Put what the user is asked at the top of the window.

<a id="notesmgr.dialogs.AskingWindow.add_buttons"></a>

#### add\_buttons

```python
def add_buttons(accept_label: str) -> None
```

Put the button that answers and the one that does not.

**Arguments**:

- `accept_label` - What the button taking the answer says.

<a id="notesmgr.dialogs.AskingWindow.accept"></a>

#### accept

```python
def accept() -> None
```

Take what the user filled in as the answer.

<a id="notesmgr.dialogs.AskingWindow.cancel"></a>

#### cancel

```python
def cancel() -> None
```

Answer nothing at all.

<a id="notesmgr.dialogs.AskingWindow.answered"></a>

#### answered

```python
def answered() -> bool
```

Wait for the answer, holding the rest of the application.

**Returns**:

  Whether the user answered rather than answering nothing.

<a id="notesmgr.dialogs.ChoiceDialog"></a>

## ChoiceDialog Objects

```python
class ChoiceDialog(AskingWindow)
```

Asks the user to choose one of several named things.

<a id="notesmgr.dialogs.ChoiceDialog.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
             question: str, options: Sequence[str]) -> None
```

Build the window that asks the question.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `question` - What the user is asked.
- `options` - What the user chooses between.

<a id="notesmgr.dialogs.ChoiceDialog.chosen"></a>

#### chosen

```python
@property
def chosen() -> Optional[str]
```

Return what was chosen, None while nothing was.

<a id="notesmgr.dialogs.ChoiceDialog.choose"></a>

#### choose

```python
def choose() -> Optional[str]
```

Wait for the answer, holding the rest of the application.

**Returns**:

  What the user chose, None when the user chose nothing.

<a id="notesmgr.dialogs.ask_choice"></a>

#### ask\_choice

```python
def ask_choice(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               question: str, options: Sequence[str]) -> Optional[str]
```

Ask the user to choose one of several named things.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `question` - What the user is asked.
- `options` - What the user chooses between.
  

**Returns**:

  What the user chose, None when the user chose nothing.

<a id="notesmgr.dialogs.ask_name"></a>

#### ask\_name

```python
def ask_name(parent: Union[tkinter.Tk, tkinter.Toplevel],
             title: str,
             question: str,
             given: str = '') -> Optional[str]
```

Ask the user for the name of a note or a folder.

What the name may be is the model's to say, so anything at all
can be typed here and is refused, if it is to be refused, where
the file is made.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `question` - What the user is asked.
- `given` - What the field holds before anything is typed.
  

**Returns**:

  What the user typed, None when the user typed nothing at all.

<a id="notesmgr.dialogs.NameFolder"></a>

## NameFolder Objects

```python
class NameFolder(NamedTuple)
```

A name, and the folder of the project that it is to be in.

<a id="notesmgr.dialogs.NameFolderDialog"></a>

## NameFolderDialog Objects

```python
class NameFolderDialog(AskingWindow)
```

Asks the user for a name and for a folder of the project.

The folders are offered to be chosen rather than to be typed, so
that what is asked for is always a folder of the project, and
the file chooser of the platform is not let anywhere near it.

<a id="notesmgr.dialogs.NameFolderDialog.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
             given: NameFolder, folders: Sequence[str]) -> None
```

Build the window that asks for the name and the folder.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `given` - What the two fields hold to begin with.
- `folders` - The folders of the project, as they are named.

<a id="notesmgr.dialogs.NameFolderDialog._fill_in"></a>

#### \_fill\_in

```python
def _fill_in(folders: Sequence[str]) -> None
```

Put the field for the name above the one for the folder.

<a id="notesmgr.dialogs.NameFolderDialog.given"></a>

#### given

```python
@property
def given() -> Optional[NameFolder]
```

Return what was filled in, None while nothing was taken.

<a id="notesmgr.dialogs.NameFolderDialog.ask_for"></a>

#### ask\_for

```python
def ask_for() -> Optional[NameFolder]
```

Wait for the answer, holding the rest of the application.

**Returns**:

  The name and the folder, None when the user gave none.

<a id="notesmgr.dialogs.ask_name_folder"></a>

#### ask\_name\_folder

```python
def ask_name_folder(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
                    given: NameFolder,
                    folders: Sequence[str]) -> Optional[NameFolder]
```

Ask the user for a name and for a folder of the project.

**Arguments**:

- `parent` - The window that the question is asked over.
- `title` - What the window asking is called.
- `given` - What the two fields hold to begin with.
- `folders` - The folders of the project, as they are named.
  

**Returns**:

  The name and the folder, None when the user gave none.

<a id="notesmgr.note_text"></a>

# notesmgr.note\_text

Reading the text of a note, and what cannot be read of it.

<a id="notesmgr.note_text.NOT_UTF8"></a>

#### NOT\_UTF8

What is said about a note that holds bytes that are no text.

<a id="notesmgr.note_text.NOT_READ"></a>

#### NOT\_READ

What is said about a note that the file system does not give.

<a id="notesmgr.note_text.TOO_LONG"></a>

#### TOO\_LONG

What is said about a note that is longer than may be shown.

<a id="notesmgr.note_text.NoteText"></a>

## NoteText Objects

```python
class NoteText(NamedTuple)
```

The text of a note, and what is to be said about it.

The warning is what the user is told above the text, and it is
empty when there is nothing to tell. A note that cannot be shown
at all has a warning and no text.

<a id="notesmgr.note_text.EMPTY_NOTE"></a>

#### EMPTY\_NOTE

What is shown when nothing at all is selected.

<a id="notesmgr.note_text.read_note_text"></a>

#### read\_note\_text

```python
def read_note_text(path: Path, limit: int) -> NoteText
```

Return the text of a note, as much of it as may be shown.

One character more than the limit is read, which is what tells a
note that fits from one that has to be cut, without reading a
note of any size into memory. Reading characters rather than
bytes is also what keeps the cut from falling inside a character.

**Arguments**:

- `path` - The note to read.
- `limit` - The most characters of it that may be shown.
  

**Returns**:

  The text to show and the warning to show above it.

<a id="notesmgr.file_watch"></a>

# notesmgr.file\_watch

Following the note that is shown while it is edited elsewhere.

<a id="notesmgr.file_watch.POLL_INTERVAL"></a>

#### POLL\_INTERVAL

Milliseconds between two looks at the note that is shown.

<a id="notesmgr.file_watch.FileState"></a>

## FileState Objects

```python
class FileState(NamedTuple)
```

What a file looked like when it was last looked at.

A file is taken to have changed when any of this is no longer
what it was, so that saving a note in an editor, deleting it and
writing it again are all seen.

<a id="notesmgr.file_watch.MISSING"></a>

#### MISSING

What a file that is not there looks like, and no file at all.

<a id="notesmgr.file_watch.file_state"></a>

#### file\_state

```python
def file_state(path: Optional[Path]) -> FileState
```

Return what a file looks like now.

A file that cannot be asked about cannot be shown either, so it
is taken to be missing rather than raising here.

**Arguments**:

- `path` - The file to look at, None for no file at all.
  

**Returns**:

  What it looks like now.

<a id="notesmgr.file_watch.FileWatch"></a>

## FileWatch Objects

```python
class FileWatch()
```

Tells whoever listens that the file being watched has changed.

The file system is asked about the file now and then, because a
note is edited by another program that notesmgr hears nothing
from. The asking is done by the Tk event loop, so the polling
holds nothing up and needs no thread of its own.

<a id="notesmgr.file_watch.FileWatch.__init__"></a>

#### \_\_init\_\_

```python
def __init__(widget: tkinter.Misc,
             on_change: Callable[[], None],
             interval: int = POLL_INTERVAL) -> None
```

Get ready to watch, watching nothing yet.

**Arguments**:

- `widget` - The widget whose event loop does the polling, and
  whose end is the end of the watching.
- `on_change` - Told whenever the watched file has changed.
- `interval` - Milliseconds between two looks at the file.

<a id="notesmgr.file_watch.FileWatch.watch"></a>

#### watch

```python
def watch(path: Optional[Path]) -> None
```

Watch another file from now on, or no file at all.

The file as it is now is what the watching starts from, so
that taking up a file is no change of it.

**Arguments**:

- `path` - The file to watch, None for no file at all.

<a id="notesmgr.file_watch.FileWatch.poll"></a>

#### poll

```python
def poll() -> None
```

Tell that the watched file has changed, when it has.

<a id="notesmgr.file_watch.FileWatch.tick"></a>

#### tick

```python
def tick() -> None
```

Look at the file again, and go on while there is a window.

<a id="notesmgr.file_watch.FileWatch.schedule"></a>

#### schedule

```python
def schedule() -> None
```

Ask for the next look, in place of one already asked for.

<a id="notesmgr.file_watch.FileWatch.cancel"></a>

#### cancel

```python
def cancel() -> None
```

Take back the look that was asked for, if there is one.

<a id="notesmgr.commands"></a>

# notesmgr.commands

What the buttons and the menu entries do to the open project.

<a id="notesmgr.commands.NOTE_TITLE"></a>

#### NOTE\_TITLE

What a window asking about or reporting about a note is called.

<a id="notesmgr.commands.FOLDER_TITLE"></a>

#### FOLDER\_TITLE

What a window asking about a folder of the project is called.

<a id="notesmgr.commands.DUPLICATE_TITLE"></a>

#### DUPLICATE\_TITLE

What the window asking where to copy a note is called.

<a id="notesmgr.commands.ASK_NEW_NOTE"></a>

#### ASK\_NEW\_NOTE

What the user is asked when making a note.

<a id="notesmgr.commands.ASK_DELETE_NOTE"></a>

#### ASK\_DELETE\_NOTE

What the user is asked before a note is taken away.

<a id="notesmgr.commands.ASK_NEW_FOLDER"></a>

#### ASK\_NEW\_FOLDER

What the user is asked when making a folder.

<a id="notesmgr.commands.ASK_RENAME_FOLDER"></a>

#### ASK\_RENAME\_FOLDER

What the user is asked when renaming a folder.

<a id="notesmgr.commands.ASK_DELETE_FOLDER"></a>

#### ASK\_DELETE\_FOLDER

What the user is asked before a folder is taken away.

<a id="notesmgr.commands.COPY_SUFFIX"></a>

#### COPY\_SUFFIX

What is put after the name of a note to name a copy of it.

<a id="notesmgr.commands.shown_folder"></a>

#### shown\_folder

```python
def shown_folder(root: Path, folder: Path) -> str
```

Return how a folder of a project is named to the user.

The root folder is named by itself and every folder below it by
the way down to it, so that two folders of the same name in
different places are told apart.

**Arguments**:

- `root` - The root folder of the project.
- `folder` - The folder of the project to name.
  

**Returns**:

  The name to show, which names the folder again through
  folder_of() when the user has chosen it.

<a id="notesmgr.commands.folder_of"></a>

#### folder\_of

```python
def folder_of(root: Path, shown: str) -> Path
```

Return the folder that a name shown to the user stands for.

<a id="notesmgr.commands.WindowHooks"></a>

## WindowHooks Objects

```python
class WindowHooks(NamedTuple)
```

What the commands ask the window that holds them to do.

The window owns the tree and the menus, so it is what shows the
project again once a command has changed it, and what offers the
actions that can be used on what is selected now.

<a id="notesmgr.commands.Commands"></a>

## Commands Objects

```python
class Commands()
```

What the buttons and the menu entries do to the open project.

Each command asks the user what it needs, has the model do it,
and has the window show the project as it now stands with what
was made or moved selected in it. What could not be done is put
to the user in the words the model said it in, and the project
is left exactly as it was.

<a id="notesmgr.commands.Commands.__init__"></a>

#### \_\_init\_\_

```python
def __init__(window: Union[tkinter.Tk, tkinter.Toplevel], session: Session,
             hooks: WindowHooks) -> None
```

Get ready to act upon a project, with nothing selected yet.

**Arguments**:

- `window` - The window that the questions are asked over.
- `session` - What the run knows, which is the open project.
- `hooks` - What the commands ask the window to do.

<a id="notesmgr.commands.Commands.select"></a>

#### select

```python
def select(path: Optional[Path]) -> None
```

Take what the explorer has selected as what to act upon.

<a id="notesmgr.commands.Commands.note_shown"></a>

#### note\_shown

```python
def note_shown(shown: bool) -> None
```

Offer afresh what can be done with what is selected.

**Arguments**:

- `shown` - Whether the panel has a note to act on, which a
  program other than notesmgr can take away at any time.

<a id="notesmgr.commands.Commands.selected"></a>

#### selected

```python
def selected(shown: bool) -> Selected
```

Return what is selected, as far as it says what can be done.

<a id="notesmgr.commands.Commands.report_error"></a>

#### report\_error

```python
def report_error(message: str) -> None
```

Tell the user what could not be done, and why it could not.

<a id="notesmgr.commands.Commands.chosen_folder"></a>

#### chosen\_folder

```python
def chosen_folder() -> Optional[Path]
```

Return the folder that is selected, None when none is.

The root folder of a project is the project itself rather
than a folder in it to be renamed or taken away, so it
counts as no folder here.

<a id="notesmgr.commands.Commands.note_folder"></a>

#### note\_folder

```python
def note_folder() -> Optional[Path]
```

Return the folder that a new note or folder goes into.

That is the selected folder, the folder of the selected note,
and the root folder of the project while nothing is selected.

<a id="notesmgr.commands.Commands.plain_note"></a>

#### plain\_note

```python
def plain_note() -> Optional[Path]
```

Return the selected note that is no template, None for none.

<a id="notesmgr.commands.Commands._extension"></a>

#### \_extension

```python
def _extension() -> Optional[NoteExtension]
```

Return the extension the notes of the open project carry.

<a id="notesmgr.commands.Commands.done"></a>

#### done

```python
def done(doing: Callable[[], Optional[Path]]) -> Optional[Path]
```

Do what changes the project, and show it as it now stands.

**Arguments**:

- `doing` - What is to be done, giving what is to be selected
  afterwards and None when it leaves nothing to select.
  

**Returns**:

  What was made or moved, None when the operation could not
  be done at all or left nothing to select.

<a id="notesmgr.commands.Commands.edit"></a>

#### edit

```python
def edit(note: Path) -> None
```

Open a note in the editor that the project is configured with.

<a id="notesmgr.commands.Commands.new_note"></a>

#### new\_note

```python
def new_note() -> None
```

Make a note from the template and open it in the editor.

<a id="notesmgr.commands.Commands.duplicate_note"></a>

#### duplicate\_note

```python
def duplicate_note() -> None
```

Copy the selected note into a folder of the project.

<a id="notesmgr.commands.Commands._ask_copy"></a>

#### \_ask\_copy

```python
def _ask_copy(note: Path, project: Project) -> Optional[NameFolder]
```

Ask what a copy of a note is called and where it is put.

<a id="notesmgr.commands.Commands._folder_names"></a>

#### \_folder\_names

```python
@staticmethod
def _folder_names(project: Project) -> Sequence[str]
```

Return the folders of a project as they are named to the user.

<a id="notesmgr.commands.Commands.delete_note"></a>

#### delete\_note

```python
def delete_note() -> None
```

Move the selected note to the trash, once the user is sure.

<a id="notesmgr.commands.Commands.move_up"></a>

#### move\_up

```python
def move_up() -> None
```

Move the selected note one place up in its folder.

<a id="notesmgr.commands.Commands.move_down"></a>

#### move\_down

```python
def move_down() -> None
```

Move the selected note one place down in its folder.

<a id="notesmgr.commands.Commands.move"></a>

#### move

```python
def move(offset: int) -> None
```

Move the selected note so many places in its folder.

<a id="notesmgr.commands.Commands.new_folder"></a>

#### new\_folder

```python
def new_folder() -> None
```

Make a folder in the folder that is selected.

<a id="notesmgr.commands.Commands.rename_folder"></a>

#### rename\_folder

```python
def rename_folder() -> None
```

Give the selected folder another name.

<a id="notesmgr.commands.Commands.delete_folder"></a>

#### delete\_folder

```python
def delete_folder() -> None
```

Move the selected folder to the trash, once the user is sure.

<a id="notesmgr.note_file"></a>

# notesmgr.note\_file

The names that the files of a notesmgr project carry.

<a id="notesmgr.note_file.TEMPLATE_STEM"></a>

#### TEMPLATE\_STEM

Name, without any extension, of the template file of a folder.

<a id="notesmgr.note_file.NOTE_EXTENSIONS"></a>

#### NOTE\_EXTENSIONS

The extensions a note file can have, the longest one first.

Trying the longest one first is what makes a name ending in .md.txt a
markdown note rather than a text note whose name ends in .md.

<a id="notesmgr.note_file.SEPARATORS"></a>

#### SEPARATORS

What a name cannot hold, because it would then name a folder too.

Both are refused on every platform, so that a project written on one
platform holds no name that another platform reads as a path.

<a id="notesmgr.note_file.NOT_IN_NAME"></a>

#### NOT\_IN\_NAME

Characters that are not allowed in a note name.

<a id="notesmgr.note_file.NO_NAME"></a>

#### NO\_NAME

What is said about a name that is empty or nothing but blanks.

<a id="notesmgr.note_file.INVALID_NAME"></a>

#### INVALID\_NAME

What is said about a name that holds invalid characters.

<a id="notesmgr.note_file.HIDDEN"></a>

#### HIDDEN

What is said about a name that would make a hidden file.

<a id="notesmgr.note_file.WRONG_EXTENSION"></a>

#### WRONG\_EXTENSION

What is said about a name carrying the extension of another project.

<a id="notesmgr.note_file.RESERVED"></a>

#### RESERVED

What is said about a note that would be taken for a template.

<a id="notesmgr.note_file.note_extension"></a>

#### note\_extension

```python
def note_extension(name: str) -> Optional[NoteExtension]
```

Return the note extension a file name carries, None for none.

A name starting with a dot is a hidden file and no note, and a
name that is nothing but an extension holds no note name at all.
The extension is recognized whatever its case, because the file
systems of macOS and Windows keep no case apart either.

**Arguments**:

- `name` - File name, without any folders before it.
  

**Returns**:

  The extension the name ends with, None when it ends with none.

<a id="notesmgr.note_file.is_note"></a>

#### is\_note

```python
def is_note(name: str) -> bool
```

Return whether a file name is the name of a note.

<a id="notesmgr.note_file.note_stem"></a>

#### note\_stem

```python
def note_stem(name: str) -> str
```

Return a note file name without the extension it ends with.

**Arguments**:

- `name` - File name of a note.
  

**Returns**:

  The name without its extension, and the name unchanged when
  it is no note name at all.

<a id="notesmgr.note_file.template_name"></a>

#### template\_name

```python
def template_name(extension: NoteExtension) -> str
```

Return what a template is called in a project of an extension.

<a id="notesmgr.note_file.is_template"></a>

#### is\_template

```python
def is_template(name: str) -> bool
```

Return whether a file name is the name of a folder's template.

<a id="notesmgr.note_file.is_plain_note"></a>

#### is\_plain\_note

```python
def is_plain_note(name: str) -> bool
```

Return whether a file name is a note that is no template.

<a id="notesmgr.note_file.name_key"></a>

#### name\_key

```python
def name_key(name: str) -> tuple[str, str]
```

Return the key that orders file names alphabetically.

Case tells two names apart only when nothing else does, so that
the order does not depend on where the names were read from.

<a id="notesmgr.note_file.sorted_names"></a>

#### sorted\_names

```python
def sorted_names(names: Iterable[str]) -> list[str]
```

Return the given file names in alphabetical order.

<a id="notesmgr.note_file.checked_extension"></a>

#### checked\_extension

```python
def checked_extension(name: str, extension: NoteExtension) -> str
```

Return a note name carrying the extension of the project.

**Arguments**:

- `name` - Name of a note, with or without an extension.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The name as it stands when it carries that extension already,
  and the name with the extension added when it carries none.
  

**Raises**:

- `NotesmgrError` - The name carries another note extension, or it
  is the name that the template of a folder has.

<a id="notesmgr.note_file.checked_name"></a>

#### checked\_name

```python
def checked_name(typed: str) -> str
```

Return the name of a file or a folder that a user typed.

**Arguments**:

- `typed` - What the user typed as a name.
  

**Returns**:

  The name with the blanks around it taken off.
  

**Raises**:

- `NotesmgrError` - What was typed names nothing that can be made
  in a folder of a project.

<a id="notesmgr.note_file.note_file_name"></a>

#### note\_file\_name

```python
def note_file_name(typed: str, extension: NoteExtension) -> str
```

Return the file name that a name typed by a user asks for.

**Arguments**:

- `typed` - What the user typed as the name of a note.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The name of the file, with the extension of the project on it.
  

**Raises**:

- `NotesmgrError` - What was typed names no note file.

<a id="notesmgr.note_view"></a>

# notesmgr.note\_view

The area of the main window that a note is read in.

<a id="notesmgr.note_view.WARNING_COLOUR"></a>

#### WARNING\_COLOUR

Colour of a warning above a note, a red that is hard to miss.

<a id="notesmgr.note_view.WARNING_FONT"></a>

#### WARNING\_FONT

Font of a warning above a note, heavier than the note itself.

<a id="notesmgr.note_view.WRAP_WIDTH"></a>

#### WRAP\_WIDTH

Pixels after which a long warning is broken into another line.

<a id="notesmgr.note_view.PADDING"></a>

#### PADDING

Space in pixels left around what the area shows.

<a id="notesmgr.note_view.TEXT_ROW"></a>

#### TEXT\_ROW

Row of the area that the note itself is shown in.

<a id="notesmgr.note_view.NoteView"></a>

## NoteView Objects

```python
class NoteView()
```

Shows the text of one note, with any warning above it.

The warning is what could not be shown and why, and it is left
out of the way whenever there is nothing to warn about. The text
is shown as it is read, because what a note looks like formatted
is what step 7 of the plan adds.

<a id="notesmgr.note_view.NoteView.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent: tkinter.Misc) -> None
```

Build the area in a frame of its own inside a parent widget.

<a id="notesmgr.note_view.NoteView._lay_out"></a>

#### \_lay\_out

```python
def _lay_out() -> None
```

Put the warning above the note and let the note have the room.

<a id="notesmgr.note_view.NoteView.show"></a>

#### show

```python
def show(note: NoteText) -> None
```

Show a note that was read, warning and all.

**Arguments**:

- `note` - The text to show and the warning to show above it.

<a id="notesmgr.note_view.NoteView.show_warning"></a>

#### show\_warning

```python
def show_warning(warning: str) -> None
```

Show a warning above the note, and none when there is none.

<a id="notesmgr.note_view.NoteView.show_text"></a>

#### show\_text

```python
def show_text(text: str) -> None
```

Show a text in an area that the user cannot type in.

<a id="notesmgr.note_view.NoteView.shown_note"></a>

#### shown\_note

```python
def shown_note() -> NoteText
```

Return the note that is shown, warning and all.

<a id="notesmgr.note_view.NoteView.area_text"></a>

#### area\_text

```python
def area_text() -> str
```

Return the text that the area holds, as the user sees it.

Tk keeps a newline of its own at the end of a text area,
which is left out here, so that what is returned is what was
put in.

<a id="notesmgr.note_view.NoteView.warning_shown"></a>

#### warning\_shown

```python
def warning_shown() -> bool
```

Return whether a warning is on the screen above the note.

<a id="notesmgr.descriptions"></a>

# notesmgr.descriptions

What notesmgr says about the members of its configuration.

<a id="notesmgr.descriptions.DESCRIPTIONS"></a>

#### DESCRIPTIONS

What each member of the configuration is for.

Python keeps no docstring of an instance attribute at runtime, so what
a member is for is said here and read by the configuration editor.

The extensions themselves are deliberately not listed here: the editor
reads them from the type of the member and lists them below its row, so
naming them here as well would be writing them twice.

<a id="notesmgr.project"></a>

# notesmgr.project

What a notesmgr project is and what the folders of it hold.

<a id="notesmgr.project.PROJECT_CONFIG"></a>

#### PROJECT\_CONFIG

Name of the configuration file in the root folder of a project.

<a id="notesmgr.project.NO_PROJECT"></a>

#### NO\_PROJECT

What is said about a folder that holds no configuration file.

<a id="notesmgr.project.NOT_LISTED"></a>

#### NOT\_LISTED

What is said about a folder whose content cannot be listed.

<a id="notesmgr.project.FolderContent"></a>

## FolderContent Objects

```python
class FolderContent(NamedTuple)
```

What one folder holds, before anything about it is repaired.

<a id="notesmgr.project.Folder"></a>

## Folder Objects

```python
class Folder(NamedTuple)
```

One folder of a project, holding what it holds in shown order.

<a id="notesmgr.project.Project"></a>

## Project Objects

```python
class Project(NamedTuple)
```

An open project: where it is, how it behaves, what it holds.

<a id="notesmgr.project.config_path"></a>

#### config\_path

```python
def config_path(root: Path) -> Path
```

Return the configuration file of the project in a folder.

<a id="notesmgr.project.is_project"></a>

#### is\_project

```python
def is_project(root: Path) -> bool
```

Return whether a folder is the root folder of a project.

<a id="notesmgr.project.read_config"></a>

#### read\_config

```python
def read_config(root: Path) -> NotesmgrConfig
```

Return the configuration of the project in a folder.

**Arguments**:

- `root` - The root folder of the project.
  

**Returns**:

  The configuration that the project is used with.
  

**Raises**:

- `NotesmgrError` - The folder is no project, or its configuration
  file holds nothing that notesmgr can use.

<a id="notesmgr.project.is_shown_folder"></a>

#### is\_shown\_folder

```python
def is_shown_folder(path: Path) -> bool
```

Return whether a folder of a project is shown in the tree.

A folder whose name starts with a dot is hidden, and a folder
reached through a symbolic link is passed over, so that a link
leading back into the project cannot make reading it go on
for ever.

<a id="notesmgr.project.folder_entries"></a>

#### folder\_entries

```python
def folder_entries(folder: Path) -> list[Path]
```

Return everything a folder holds, in alphabetical order.

**Arguments**:

- `folder` - Folder of a project.
  

**Returns**:

  Every file and folder in it, hidden ones and all, because
  what is shown is one question and what a name would collide
  with is another.
  

**Raises**:

- `NotesmgrError` - The folder cannot be read.

<a id="notesmgr.project.folder_content"></a>

#### folder\_content

```python
def folder_content(folder: Path) -> FolderContent
```

Return what a folder holds, in the order it is shown in.

**Arguments**:

- `folder` - Folder of a project.
  

**Returns**:

  The subfolders and the templates in alphabetical order, and
  the names of the notes in the order the folder happened to
  give them, which the note order file has yet to settle.
  

**Raises**:

- `NotesmgrError` - The folder cannot be read.

<a id="notesmgr.project.folder_paths"></a>

#### folder\_paths

```python
def folder_paths(folder: Folder) -> list[Path]
```

Return a folder of a project and every folder below it.

**Arguments**:

- `folder` - The folder to start from, which is the tree of the
  project when every folder of it is wanted.
  

**Returns**:

  The folders, each one before the folders below it, which is
  the order that the explorer shows them in.

<a id="notesmgr.folder_ops"></a>

# notesmgr.folder\_ops

Making, renaming and taking away the folders of a project.

<a id="notesmgr.folder_ops.IS_PROJECT"></a>

#### IS\_PROJECT

What is said about the root folder, which is no folder to change.

<a id="notesmgr.folder_ops.NOT_EMPTY"></a>

#### NOT\_EMPTY

What is said about a folder that is not to be taken away yet.

<a id="notesmgr.folder_ops.NOT_MADE"></a>

#### NOT\_MADE

What is said about a folder that the file system would not take.

<a id="notesmgr.folder_ops.NOT_RENAMED"></a>

#### NOT\_RENAMED

What is said about a folder that could not be given its new name.

<a id="notesmgr.folder_ops.NOT_TRASHED"></a>

#### NOT\_TRASHED

What is said about a folder that the trash would not take.

<a id="notesmgr.folder_ops.new_folder"></a>

#### new\_folder

```python
def new_folder(parent: Path, typed: str, extension: NoteExtension) -> Path
```

Make a folder in a folder of the project.

The new folder starts out as the folder above it: it is given a
copy of that folder's template and a note order file of its own,
so that opening the project again finds nothing to repair.

**Arguments**:

- `parent` - The folder that the new folder is made in.
- `typed` - What the user typed as the name of the new folder.
- `extension` - The extension that the notes of the project have.
  

**Returns**:

  The folder that was made.
  

**Raises**:

- `NotesmgrError` - The name names no folder that can be made
  here, or the folder cannot be made.

<a id="notesmgr.folder_ops.rename_folder"></a>

#### rename\_folder

```python
def rename_folder(folder: Path, typed: str) -> Path
```

Give a folder of the project another name.

Nothing outside a folder names it, so a folder is renamed whether
it holds anything or not. The root folder is the project itself
rather than a folder in it, and is renamed from the outside.

**Arguments**:

- `folder` - The folder to rename.
- `typed` - What the user typed as its new name.
  

**Returns**:

  The folder under the name it now has.
  

**Raises**:

- `NotesmgrError` - The folder is the root folder of the project,
  the name names no folder, the name is taken already, or
  the folder cannot be renamed.

<a id="notesmgr.folder_ops.is_empty"></a>

#### is\_empty

```python
def is_empty(folder: Path) -> bool
```

Return whether a folder holds nothing but notesmgr's own files.

The template of a folder and its note order file are notesmgr's
doing rather than anything the user put there, so a folder that
holds only those is empty to the user who is looking at it.

**Arguments**:

- `folder` - The folder to look into.
  

**Returns**:

  Whether nothing of the user's would be taken away with it.
  

**Raises**:

- `NotesmgrError` - The folder cannot be read.

<a id="notesmgr.folder_ops.delete_folder"></a>

#### delete\_folder

```python
def delete_folder(folder: Path) -> None
```

Move a folder that holds nothing of the user's to the trash.

**Arguments**:

- `folder` - The folder to take away.
  

**Raises**:

- `NotesmgrError` - The folder is the root folder of the project,
  it holds notes or folders of its own, or the trash would
  not take it.


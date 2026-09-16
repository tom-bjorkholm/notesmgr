# Table of Contents

* [notesmgr.main\_window](#notesmgr.main_window)
  * [Shortcut](#notesmgr.main_window.Shortcut)
  * [Shortcuts](#notesmgr.main_window.Shortcuts)
  * [tk\_window\_system](#notesmgr.main_window.tk_window_system)
  * [quit\_shortcut](#notesmgr.main_window.quit_shortcut)
  * [modifier](#notesmgr.main_window.modifier)
  * [held\_shortcut](#notesmgr.main_window.held_shortcut)
  * [window\_shortcuts](#notesmgr.main_window.window_shortcuts)
  * [MainWindow](#notesmgr.main_window.MainWindow)
    * [\_\_init\_\_](#notesmgr.main_window.MainWindow.__init__)
    * [\_menu\_specs](#notesmgr.main_window.MainWindow._menu_specs)
    * [\_note\_entries](#notesmgr.main_window.MainWindow._note_entries)
    * [\_folder\_entries](#notesmgr.main_window.MainWindow._folder_entries)
    * [\_view\_entries](#notesmgr.main_window.MainWindow._view_entries)
    * [\_zoom\_command](#notesmgr.main_window.MainWindow._zoom_command)
    * [\_normal\_command](#notesmgr.main_window.MainWindow._normal_command)
    * [zoom](#notesmgr.main_window.MainWindow.zoom)
    * [zoom\_normal](#notesmgr.main_window.MainWindow.zoom_normal)
    * [\_bind\_shortcuts](#notesmgr.main_window.MainWindow._bind_shortcuts)
    * [\_bind](#notesmgr.main_window.MainWindow._bind)
    * [\_shape\_window](#notesmgr.main_window.MainWindow._shape_window)
    * [show\_project](#notesmgr.main_window.MainWindow.show_project)
    * [show\_selected](#notesmgr.main_window.MainWindow.show_selected)
    * [dropped](#notesmgr.main_window.MainWindow.dropped)
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
* [notesmgr.note\_blocks](#notesmgr.note_blocks)
  * [SpanStyle](#notesmgr.note_blocks.SpanStyle)
  * [BlockKind](#notesmgr.note_blocks.BlockKind)
  * [Span](#notesmgr.note_blocks.Span)
  * [Block](#notesmgr.note_blocks.Block)
  * [HEADINGS](#notesmgr.note_blocks.HEADINGS)
  * [STYLES](#notesmgr.note_blocks.STYLES)
  * [CONTAINERS](#notesmgr.note_blocks.CONTAINERS)
  * [TEXT\_TAGS](#notesmgr.note_blocks.TEXT_TAGS)
  * [TABLE\_TAGS](#notesmgr.note_blocks.TABLE_TAGS)
  * [CELL\_TAGS](#notesmgr.note_blocks.CELL_TAGS)
  * [BULLETS](#notesmgr.note_blocks.BULLETS)
  * [BLANKS](#notesmgr.note_blocks.BLANKS)
  * [squeezed](#notesmgr.note_blocks.squeezed)
  * [kept](#notesmgr.note_blocks.kept)
  * [trimmed](#notesmgr.note_blocks.trimmed)
  * [Container](#notesmgr.note_blocks.Container)
  * [OpenBlock](#notesmgr.note_blocks.OpenBlock)
  * [OpenStyles](#notesmgr.note_blocks.OpenStyles)
  * [TableReader](#notesmgr.note_blocks.TableReader)
    * [start\_row](#notesmgr.note_blocks.TableReader.start_row)
    * [start\_cell](#notesmgr.note_blocks.TableReader.start_cell)
    * [add\_text](#notesmgr.note_blocks.TableReader.add_text)
    * [end\_cell](#notesmgr.note_blocks.TableReader.end_cell)
    * [text](#notesmgr.note_blocks.TableReader.text)
  * [item\_prefix](#notesmgr.note_blocks.item_prefix)
  * [NoteParser](#notesmgr.note_blocks.NoteParser)
    * [\_\_init\_\_](#notesmgr.note_blocks.NoteParser.__init__)
    * [note\_blocks](#notesmgr.note_blocks.NoteParser.note_blocks)
    * [handle\_starttag](#notesmgr.note_blocks.NoteParser.handle_starttag)
    * [handle\_endtag](#notesmgr.note_blocks.NoteParser.handle_endtag)
    * [handle\_data](#notesmgr.note_blocks.NoteParser.handle_data)
    * [\_open\_other](#notesmgr.note_blocks.NoteParser._open_other)
    * [\_depth](#notesmgr.note_blocks.NoteParser._depth)
    * [\_text\_kind](#notesmgr.note_blocks.NoteParser._text_kind)
    * [\_open\_block](#notesmgr.note_blocks.NoteParser._open_block)
    * [\_block\_spans](#notesmgr.note_blocks.NoteParser._block_spans)
    * [\_flush](#notesmgr.note_blocks.NoteParser._flush)
    * [\_open\_container](#notesmgr.note_blocks.NoteParser._open_container)
    * [\_close\_container](#notesmgr.note_blocks.NoteParser._close_container)
    * [\_open\_item](#notesmgr.note_blocks.NoteParser._open_item)
    * [\_open\_code](#notesmgr.note_blocks.NoteParser._open_code)
    * [\_close\_code](#notesmgr.note_blocks.NoteParser._close_code)
    * [\_open\_style](#notesmgr.note_blocks.NoteParser._open_style)
    * [\_close\_style](#notesmgr.note_blocks.NoteParser._close_style)
    * [\_open\_link](#notesmgr.note_blocks.NoteParser._open_link)
    * [\_close\_link](#notesmgr.note_blocks.NoteParser._close_link)
    * [\_add\_text](#notesmgr.note_blocks.NoteParser._add_text)
    * [\_read](#notesmgr.note_blocks.NoteParser._read)
    * [\_after\_break](#notesmgr.note_blocks.NoteParser._after_break)
    * [\_span](#notesmgr.note_blocks.NoteParser._span)
    * [\_add\_break](#notesmgr.note_blocks.NoteParser._add_break)
    * [\_add\_image](#notesmgr.note_blocks.NoteParser._add_image)
    * [\_add\_rule](#notesmgr.note_blocks.NoteParser._add_rule)
    * [\_open\_table\_tag](#notesmgr.note_blocks.NoteParser._open_table_tag)
    * [\_close\_table\_tag](#notesmgr.note_blocks.NoteParser._close_table_tag)
    * [\_open\_table](#notesmgr.note_blocks.NoteParser._open_table)
    * [\_close\_table](#notesmgr.note_blocks.NoteParser._close_table)
  * [html\_blocks](#notesmgr.note_blocks.html_blocks)
  * [markdown\_blocks](#notesmgr.note_blocks.markdown_blocks)
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
* [notesmgr.explorer\_drop](#notesmgr.explorer_drop)
  * [Drop](#notesmgr.explorer_drop.Drop)
  * [folder\_drop](#notesmgr.explorer_drop.folder_drop)
  * [note\_place](#notesmgr.explorer_drop.note_place)
  * [stays\_put](#notesmgr.explorer_drop.stays_put)
  * [dragged\_note](#notesmgr.explorer_drop.dragged_note)
  * [note\_drop](#notesmgr.explorer_drop.note_drop)
  * [drop\_target](#notesmgr.explorer_drop.drop_target)
  * [drop\_item](#notesmgr.explorer_drop.drop_item)
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
  * [NOT\_MOVED](#notesmgr.note_ops.NOT_MOVED)
  * [resync\_order](#notesmgr.note_ops.resync_order)
  * [free\_path](#notesmgr.note_ops.free_path)
  * [new\_path](#notesmgr.note_ops.new_path)
  * [template\_text](#notesmgr.note_ops.template_text)
  * [new\_note](#notesmgr.note_ops.new_note)
  * [duplicate\_note](#notesmgr.note_ops.duplicate_note)
  * [delete\_note](#notesmgr.note_ops.delete_note)
  * [moved\_order](#notesmgr.note_ops.moved_order)
  * [moved\_to](#notesmgr.note_ops.moved_to)
  * [reordered](#notesmgr.note_ops.reordered)
  * [shift\_note](#notesmgr.note_ops.shift_note)
  * [place\_note](#notesmgr.note_ops.place_note)
  * [move\_note](#notesmgr.note_ops.move_note)
* [notesmgr.clipboard\_linux](#notesmgr.clipboard_linux)
  * [XCLIP](#notesmgr.clipboard_linux.XCLIP)
  * [WL\_COPY](#notesmgr.clipboard_linux.WL_COPY)
  * [TOOLS](#notesmgr.clipboard_linux.TOOLS)
  * [NO\_TOOL](#notesmgr.clipboard_linux.NO_TOOL)
  * [CHARSET](#notesmgr.clipboard_linux.CHARSET)
  * [html\_tool](#notesmgr.clipboard_linux.html_tool)
  * [copy\_to\_clipboard](#notesmgr.clipboard_linux.copy_to_clipboard)
* [notesmgr.clipboard\_windows](#notesmgr.clipboard_windows)
  * [HEADER](#notesmgr.clipboard_windows.HEADER)
  * [OPENING](#notesmgr.clipboard_windows.OPENING)
  * [CLOSING](#notesmgr.clipboard_windows.CLOSING)
  * [HTML\_FORMAT](#notesmgr.clipboard_windows.HTML_FORMAT)
  * [UNICODE\_TEXT](#notesmgr.clipboard_windows.UNICODE_TEXT)
  * [MOVEABLE](#notesmgr.clipboard_windows.MOVEABLE)
  * [NOT\_WINDOWS](#notesmgr.clipboard_windows.NOT_WINDOWS)
  * [NOT\_OPENED](#notesmgr.clipboard_windows.NOT_OPENED)
  * [NO\_MEMORY](#notesmgr.clipboard_windows.NO_MEMORY)
  * [byte\_length](#notesmgr.clipboard_windows.byte_length)
  * [cf\_html](#notesmgr.clipboard_windows.cf_html)
  * [html\_bytes](#notesmgr.clipboard_windows.html_bytes)
  * [text\_bytes](#notesmgr.clipboard_windows.text_bytes)
  * [moveable\_memory](#notesmgr.clipboard_windows.moveable_memory)
  * [write\_clipboard](#notesmgr.clipboard_windows.write_clipboard)
  * [copy\_to\_clipboard](#notesmgr.clipboard_windows.copy_to_clipboard)
* [notesmgr.rich\_clipboard](#notesmgr.rich_clipboard)
  * [PLAIN](#notesmgr.rich_clipboard.PLAIN)
  * [IMAGE\_SOURCE](#notesmgr.rich_clipboard.IMAGE_SOURCE)
  * [BACKENDS](#notesmgr.rich_clipboard.BACKENDS)
  * [absolute\_source](#notesmgr.rich_clipboard.absolute_source)
  * [local\_images](#notesmgr.rich_clipboard.local_images)
  * [note\_fragment](#notesmgr.rich_clipboard.note_fragment)
  * [note\_rich\_text](#notesmgr.rich_clipboard.note_rich_text)
  * [backend](#notesmgr.rich_clipboard.backend)
  * [copy\_rich](#notesmgr.rich_clipboard.copy_rich)
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
* [notesmgr.note\_tags](#notesmgr.note_tags)
  * [CODE\_BACKGROUND](#notesmgr.note_tags.CODE_BACKGROUND)
  * [QUOTE\_COLOUR](#notesmgr.note_tags.QUOTE_COLOUR)
  * [LINK\_COLOUR](#notesmgr.note_tags.LINK_COLOUR)
  * [RULE\_COLOUR](#notesmgr.note_tags.RULE_COLOUR)
  * [LINK\_TAG](#notesmgr.note_tags.LINK_TAG)
  * [CODE\_SPAN\_TAG](#notesmgr.note_tags.CODE_SPAN_TAG)
  * [STRIKE\_TAG](#notesmgr.note_tags.STRIKE_TAG)
  * [IMAGE\_TAG](#notesmgr.note_tags.IMAGE_TAG)
  * [GAP\_TAG](#notesmgr.note_tags.GAP_TAG)
  * [INDENT\_TAG](#notesmgr.note_tags.INDENT_TAG)
  * [ITEM\_TAG](#notesmgr.note_tags.ITEM_TAG)
  * [MAX\_INDENT](#notesmgr.note_tags.MAX_INDENT)
  * [RAW\_KEY](#notesmgr.note_tags.RAW_KEY)
  * [GAP\_KEY](#notesmgr.note_tags.GAP_KEY)
  * [HEADING\_GAPS](#notesmgr.note_tags.HEADING_GAPS)
  * [BULLET\_ROOM](#notesmgr.note_tags.BULLET_ROOM)
  * [indent\_tag](#notesmgr.note_tags.indent_tag)
  * [gap\_lines](#notesmgr.note_tags.gap_lines)
  * [span\_styles](#notesmgr.note_tags.span_styles)
  * [NoteTags](#notesmgr.note_tags.NoteTags)
    * [\_\_init\_\_](#notesmgr.note_tags.NoteTags.__init__)
    * [\_colour\_tags](#notesmgr.note_tags.NoteTags._colour_tags)
    * [\_sized\_tags](#notesmgr.note_tags.NoteTags._sized_tags)
    * [font\_tag\_of](#notesmgr.note_tags.NoteTags.font_tag_of)
    * [span\_tags](#notesmgr.note_tags.NoteTags.span_tags)
    * [resize](#notesmgr.note_tags.NoteTags.resize)
    * [zoom](#notesmgr.note_tags.NoteTags.zoom)
    * [normal\_size](#notesmgr.note_tags.NoteTags.normal_size)
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
* [notesmgr.note\_table](#notesmgr.note_table)
  * [MAX\_COLUMN](#notesmgr.note_table.MAX_COLUMN)
  * [CELL\_GAP](#notesmgr.note_table.CELL_GAP)
  * [RULE\_GAP](#notesmgr.note_table.RULE_GAP)
  * [RULE\_CHAR](#notesmgr.note_table.RULE_CHAR)
  * [Align](#notesmgr.note_table.Align)
  * [cell\_align](#notesmgr.note_table.cell_align)
  * [squared](#notesmgr.note_table.squared)
  * [every\_align](#notesmgr.note_table.every_align)
  * [column\_width](#notesmgr.note_table.column_width)
  * [wrapped\_cell](#notesmgr.note_table.wrapped_cell)
  * [line\_at](#notesmgr.note_table.line_at)
  * [padded\_cell](#notesmgr.note_table.padded_cell)
  * [row\_lines](#notesmgr.note_table.row_lines)
  * [rule\_line](#notesmgr.note_table.rule_line)
  * [table\_text](#notesmgr.note_table.table_text)
* [notesmgr.note\_fonts](#notesmgr.note_fonts)
  * [MIN\_SIZE](#notesmgr.note_fonts.MIN_SIZE)
  * [MAX\_SIZE](#notesmgr.note_fonts.MAX_SIZE)
  * [FALLBACK\_SIZE](#notesmgr.note_fonts.FALLBACK_SIZE)
  * [TEXT\_FONT](#notesmgr.note_fonts.TEXT_FONT)
  * [FIXED\_FONT](#notesmgr.note_fonts.FIXED_FONT)
  * [BODY\_SCALE](#notesmgr.note_fonts.BODY_SCALE)
  * [FIXED\_KINDS](#notesmgr.note_fonts.FIXED_KINDS)
  * [HEADING\_SCALES](#notesmgr.note_fonts.HEADING_SCALES)
  * [note\_size](#notesmgr.note_fonts.note_size)
  * [default\_size](#notesmgr.note_fonts.default_size)
  * [family\_of](#notesmgr.note_fonts.family_of)
  * [FontKey](#notesmgr.note_fonts.FontKey)
  * [BODY\_KEY](#notesmgr.note_fonts.BODY_KEY)
  * [font\_key](#notesmgr.note_fonts.font_key)
  * [font\_tag](#notesmgr.note_fonts.font_tag)
  * [NoteFonts](#notesmgr.note_fonts.NoteFonts)
    * [\_\_init\_\_](#notesmgr.note_fonts.NoteFonts.__init__)
    * [font](#notesmgr.note_fonts.NoteFonts.font)
    * [\_make](#notesmgr.note_fonts.NoteFonts._make)
    * [scaled](#notesmgr.note_fonts.NoteFonts.scaled)
    * [resize](#notesmgr.note_fonts.NoteFonts.resize)
    * [zoom](#notesmgr.note_fonts.NoteFonts.zoom)
    * [normal\_size](#notesmgr.note_fonts.NoteFonts.normal_size)
    * [indent\_step](#notesmgr.note_fonts.NoteFonts.indent_step)
* [notesmgr.note\_panel](#notesmgr.note_panel)
  * [PADDING](#notesmgr.note_panel.PADDING)
  * [PLAIN\_INSTEAD](#notesmgr.note_panel.PLAIN_INSTEAD)
  * [NotePanel](#notesmgr.note_panel.NotePanel)
    * [\_\_init\_\_](#notesmgr.note_panel.NotePanel.__init__)
    * [\_button\_specs](#notesmgr.note_panel.NotePanel._button_specs)
    * [actions](#notesmgr.note_panel.NotePanel.actions)
    * [note\_limit](#notesmgr.note_panel.NotePanel.note_limit)
    * [note\_path](#notesmgr.note_panel.NotePanel.note_path)
    * [has\_note](#notesmgr.note_panel.NotePanel.has_note)
    * [show\_path](#notesmgr.note_panel.NotePanel.show_path)
    * [reload](#notesmgr.note_panel.NotePanel.reload)
    * [zoom](#notesmgr.note_panel.NotePanel.zoom)
    * [zoom\_normal](#notesmgr.note_panel.NotePanel.zoom_normal)
    * [offer](#notesmgr.note_panel.NotePanel.offer)
    * [shown\_path](#notesmgr.note_panel.NotePanel.shown_path)
    * [edit\_note](#notesmgr.note_panel.NotePanel.edit_note)
    * [copied\_note](#notesmgr.note_panel.NotePanel.copied_note)
    * [put\_on\_clipboard](#notesmgr.note_panel.NotePanel.put_on_clipboard)
    * [copy\_raw](#notesmgr.note_panel.NotePanel.copy_raw)
    * [copy\_formatted](#notesmgr.note_panel.NotePanel.copy_formatted)
* [notesmgr.markdown\_render](#notesmgr.markdown_render)
  * [EXTENSIONS](#notesmgr.markdown_render.EXTENSIONS)
  * [STRIKE\_PATTERN](#notesmgr.markdown_render.STRIKE_PATTERN)
  * [STRIKE\_TAG](#notesmgr.markdown_render.STRIKE_TAG)
  * [STRIKE\_NAME](#notesmgr.markdown_render.STRIKE_NAME)
  * [STRIKE\_PRIORITY](#notesmgr.markdown_render.STRIKE_PRIORITY)
  * [TAB\_LENGTH](#notesmgr.markdown_render.TAB_LENGTH)
  * [markdown\_converter](#notesmgr.markdown_render.markdown_converter)
  * [note\_html](#notesmgr.markdown_render.note_html)
* [notesmgr.explorer\_drag](#notesmgr.explorer_drag)
  * [PRESS\_EVENT](#notesmgr.explorer_drag.PRESS_EVENT)
  * [MOTION\_EVENT](#notesmgr.explorer_drag.MOTION_EVENT)
  * [RELEASE\_EVENT](#notesmgr.explorer_drag.RELEASE_EVENT)
  * [CANCEL\_EVENT](#notesmgr.explorer_drag.CANCEL_EVENT)
  * [DRAG\_START](#notesmgr.explorer_drag.DRAG_START)
  * [MARK\_TAG](#notesmgr.explorer_drag.MARK_TAG)
  * [MARK\_COLOUR](#notesmgr.explorer_drag.MARK_COLOUR)
  * [MARK\_TEXT\_COLOUR](#notesmgr.explorer_drag.MARK_TEXT_COLOUR)
  * [LINE\_HEIGHT](#notesmgr.explorer_drag.LINE_HEIGHT)
  * [Dragging](#notesmgr.explorer_drag.Dragging)
  * [row\_at](#notesmgr.explorer_drag.row_at)
  * [row\_box](#notesmgr.explorer_drag.row_box)
  * [lower\_half](#notesmgr.explorer_drag.lower_half)
  * [DropMark](#notesmgr.explorer_drag.DropMark)
    * [\_\_init\_\_](#notesmgr.explorer_drag.DropMark.__init__)
    * [at\_folder](#notesmgr.explorer_drag.DropMark.at_folder)
    * [at\_edge](#notesmgr.explorer_drag.DropMark.at_edge)
    * [clear](#notesmgr.explorer_drag.DropMark.clear)
  * [ExplorerDrag](#notesmgr.explorer_drag.ExplorerDrag)
    * [\_\_init\_\_](#notesmgr.explorer_drag.ExplorerDrag.__init__)
    * [press](#notesmgr.explorer_drag.ExplorerDrag.press)
    * [motion](#notesmgr.explorer_drag.ExplorerDrag.motion)
    * [release](#notesmgr.explorer_drag.ExplorerDrag.release)
    * [cancelled](#notesmgr.explorer_drag.ExplorerDrag.cancelled)
    * [cancel](#notesmgr.explorer_drag.ExplorerDrag.cancel)
    * [dragging](#notesmgr.explorer_drag.ExplorerDrag.dragging)
    * [show](#notesmgr.explorer_drag.ExplorerDrag.show)
* [notesmgr.explorer\_font](#notesmgr.explorer_font)
  * [ROW\_PADDING](#notesmgr.explorer_font.ROW_PADDING)
  * [STYLE\_KIND](#notesmgr.explorer_font.STYLE_KIND)
  * [STYLE\_NUMBERS](#notesmgr.explorer_font.STYLE_NUMBERS)
  * [TreeFont](#notesmgr.explorer_font.TreeFont)
    * [\_\_init\_\_](#notesmgr.explorer_font.TreeFont.__init__)
    * [apply](#notesmgr.explorer_font.TreeFont.apply)
    * [row\_height](#notesmgr.explorer_font.TreeFont.row_height)
    * [resize](#notesmgr.explorer_font.TreeFont.resize)
    * [zoom](#notesmgr.explorer_font.TreeFont.zoom)
    * [normal\_size](#notesmgr.explorer_font.TreeFont.normal_size)
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
* [notesmgr.note\_image](#notesmgr.note_image)
  * [MAX\_IMAGE\_WIDTH](#notesmgr.note_image.MAX_IMAGE_WIDTH)
  * [is\_remote](#notesmgr.note_image.is_remote)
  * [image\_path](#notesmgr.note_image.image_path)
  * [shrink\_factor](#notesmgr.note_image.shrink_factor)
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
    * [drop\_at](#notesmgr.explorer_tree.ExplorerTree.drop_at)
    * [zoom](#notesmgr.explorer_tree.ExplorerTree.zoom)
    * [zoom\_normal](#notesmgr.explorer_tree.ExplorerTree.zoom_normal)
    * [show](#notesmgr.explorer_tree.ExplorerTree.show)
    * [add\_folder](#notesmgr.explorer_tree.ExplorerTree.add_folder)
    * [shown\_files](#notesmgr.explorer_tree.ExplorerTree.shown_files)
* [notesmgr.errors](#notesmgr.errors)
  * [NotesmgrError](#notesmgr.errors.NotesmgrError)
* [notesmgr.clipboard\_macos](#notesmgr.clipboard_macos)
  * [TEXTUTIL](#notesmgr.clipboard_macos.TEXTUTIL)
  * [SCRIPT](#notesmgr.clipboard_macos.SCRIPT)
  * [OSASCRIPT](#notesmgr.clipboard_macos.OSASCRIPT)
  * [RTF\_NAME](#notesmgr.clipboard_macos.RTF_NAME)
  * [TEXT\_NAME](#notesmgr.clipboard_macos.TEXT_NAME)
  * [written](#notesmgr.clipboard_macos.written)
  * [copy\_to\_clipboard](#notesmgr.clipboard_macos.copy_to_clipboard)
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
* [notesmgr.clipboard\_tool](#notesmgr.clipboard_tool)
  * [NOT\_INSTALLED](#notesmgr.clipboard_tool.NOT_INSTALLED)
  * [REFUSED](#notesmgr.clipboard_tool.REFUSED)
  * [RichText](#notesmgr.clipboard_tool.RichText)
  * [said\_by](#notesmgr.clipboard_tool.said_by)
  * [run\_tool](#notesmgr.clipboard_tool.run_tool)
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
    * [report\_notice](#notesmgr.commands.Commands.report_notice)
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
    * [drop](#notesmgr.commands.Commands.drop)
    * [new\_folder](#notesmgr.commands.Commands.new_folder)
    * [rename\_folder](#notesmgr.commands.Commands.rename_folder)
    * [delete\_folder](#notesmgr.commands.Commands.delete_folder)
* [notesmgr.note\_file](#notesmgr.note_file)
  * [TEMPLATE\_STEM](#notesmgr.note_file.TEMPLATE_STEM)
  * [NOTE\_EXTENSIONS](#notesmgr.note_file.NOTE_EXTENSIONS)
  * [MARKDOWN\_EXTENSIONS](#notesmgr.note_file.MARKDOWN_EXTENSIONS)
  * [SEPARATORS](#notesmgr.note_file.SEPARATORS)
  * [NOT\_IN\_NAME](#notesmgr.note_file.NOT_IN_NAME)
  * [NO\_NAME](#notesmgr.note_file.NO_NAME)
  * [INVALID\_NAME](#notesmgr.note_file.INVALID_NAME)
  * [HIDDEN](#notesmgr.note_file.HIDDEN)
  * [WRONG\_EXTENSION](#notesmgr.note_file.WRONG_EXTENSION)
  * [RESERVED](#notesmgr.note_file.RESERVED)
  * [note\_extension](#notesmgr.note_file.note_extension)
  * [is\_note](#notesmgr.note_file.is_note)
  * [is\_markdown](#notesmgr.note_file.is_markdown)
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
  * [RULE\_TEXT](#notesmgr.note_view.RULE_TEXT)
  * [IMAGE\_TEXT](#notesmgr.note_view.IMAGE_TEXT)
  * [MISSING\_ALT](#notesmgr.note_view.MISSING_ALT)
  * [IMAGE\_PADDING](#notesmgr.note_view.IMAGE_PADDING)
  * [block\_spans](#notesmgr.note_view.block_spans)
  * [image\_text](#notesmgr.note_view.image_text)
  * [NoteView](#notesmgr.note_view.NoteView)
    * [\_\_init\_\_](#notesmgr.note_view.NoteView.__init__)
    * [\_lay\_out](#notesmgr.note_view.NoteView._lay_out)
    * [show](#notesmgr.note_view.NoteView.show)
    * [show\_warning](#notesmgr.note_view.NoteView.show_warning)
    * [\_writing](#notesmgr.note_view.NoteView._writing)
    * [show\_text](#notesmgr.note_view.NoteView.show_text)
    * [show\_blocks](#notesmgr.note_view.NoteView.show_blocks)
    * [\_write\_gap](#notesmgr.note_view.NoteView._write_gap)
    * [\_write\_block](#notesmgr.note_view.NoteView._write_block)
    * [\_write\_span](#notesmgr.note_view.NoteView._write_span)
    * [\_write\_text](#notesmgr.note_view.NoteView._write_text)
    * [\_draw\_picture](#notesmgr.note_view.NoteView._draw_picture)
    * [\_picture](#notesmgr.note_view.NoteView._picture)
    * [\_fitted](#notesmgr.note_view.NoteView._fitted)
    * [zoom](#notesmgr.note_view.NoteView.zoom)
    * [zoom\_normal](#notesmgr.note_view.NoteView.zoom_normal)
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
  * [folder\_at](#notesmgr.project.folder_at)
* [notesmgr.folder\_ops](#notesmgr.folder_ops)
  * [IS\_PROJECT](#notesmgr.folder_ops.IS_PROJECT)
  * [NOT\_EMPTY](#notesmgr.folder_ops.NOT_EMPTY)
  * [NOT\_MADE](#notesmgr.folder_ops.NOT_MADE)
  * [NOT\_RENAMED](#notesmgr.folder_ops.NOT_RENAMED)
  * [NOT\_TRASHED](#notesmgr.folder_ops.NOT_TRASHED)
  * [NOT\_MOVED](#notesmgr.folder_ops.NOT_MOVED)
  * [INTO\_ITSELF](#notesmgr.folder_ops.INTO_ITSELF)
  * [new\_folder](#notesmgr.folder_ops.new_folder)
  * [rename\_folder](#notesmgr.folder_ops.rename_folder)
  * [is\_empty](#notesmgr.folder_ops.is_empty)
  * [delete\_folder](#notesmgr.folder_ops.delete_folder)
  * [move\_folder](#notesmgr.folder_ops.move_folder)

<a id="notesmgr.main_window"></a>

# notesmgr.main\_window

The main window of the notesmgr application.

<a id="notesmgr.main_window.Shortcut"></a>

## Shortcut Objects

```python
class Shortcut(NamedTuple)
```

A keyboard shortcut: its Tk event sequences and its menu label.

A shortcut has more than one sequence wherever more than one key
stands for it, such as the plus of the keypad and the plus that
is typed with the shift key held down.

<a id="notesmgr.main_window.Shortcuts"></a>

## Shortcuts Objects

```python
class Shortcuts(NamedTuple)
```

The keyboard shortcuts that the main window listens for.

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

<a id="notesmgr.main_window.modifier"></a>

#### modifier

```python
def modifier(window_system: str) -> tuple[str, str]
```

Return the key held down for a shortcut, and what it is called.

macOS holds the command key down where Windows and the X11
desktops hold the control key down.

<a id="notesmgr.main_window.held_shortcut"></a>

#### held\_shortcut

```python
def held_shortcut(window_system: str, keysyms: Sequence[str],
                  shown: str) -> Shortcut
```

Return a shortcut of the held key and the keys that stand for it.

**Arguments**:

- `window_system` - The windowing system that Tk is using.
- `keysyms` - What Tk calls each of the keys that stand for it.
- `shown` - What the key is called on the menu entry.
  

**Returns**:

  The shortcut to bind and to show.

<a id="notesmgr.main_window.window_shortcuts"></a>

#### window\_shortcuts

```python
def window_shortcuts(window_system: str) -> Shortcuts
```

Return the shortcuts of the main window on a windowing system.

Making a note larger is asked for with a plus, which is typed
with the shift key held down on most keyboards and is a key of
its own on the keypad, so every key that stands for it is bound
and the plainest of them is the one that is shown.

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
def _menu_specs(keys: Shortcuts) -> list[MenuSpec]
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
buttons. A button that was described with no command has
nothing to do, and is left out of the menu until it has.

<a id="notesmgr.main_window.MainWindow._folder_entries"></a>

#### \_folder\_entries

```python
def _folder_entries() -> list[MenuEntry]
```

Return the entries that act on a folder of the project.

<a id="notesmgr.main_window.MainWindow._view_entries"></a>

#### \_view\_entries

```python
def _view_entries(keys: Shortcuts) -> list[MenuEntry]
```

Return the entries that say how large a note is drawn.

A note is read on whatever screen the user has, so how large
it is drawn is theirs to say, and it can always be said
however small or large the note itself is.

<a id="notesmgr.main_window.MainWindow._zoom_command"></a>

#### \_zoom\_command

```python
def _zoom_command(step: int) -> Callable[[], None]
```

Return what draws the window so many steps larger or smaller.

<a id="notesmgr.main_window.MainWindow._normal_command"></a>

#### \_normal\_command

```python
def _normal_command() -> Callable[[], None]
```

Return what draws the window in the size it started out in.

<a id="notesmgr.main_window.MainWindow.zoom"></a>

#### zoom

```python
def zoom(step: int) -> None
```

Draw the note and the tree so many steps larger or smaller.

The note and the names of the notes are read on one screen
and at one distance from it, so they are made larger and
smaller together rather than each for itself.

<a id="notesmgr.main_window.MainWindow.zoom_normal"></a>

#### zoom\_normal

```python
def zoom_normal() -> None
```

Draw the note and the tree in the size they started out in.

<a id="notesmgr.main_window.MainWindow._bind_shortcuts"></a>

#### \_bind\_shortcuts

```python
def _bind_shortcuts(keys: Shortcuts) -> None
```

Let the shortcuts shown on the menu entries be typed.

Tk installs no binding for a menu accelerator, so every key
sequence has to be bound as well. They are bound on this
window only, so that a dialog which happens to have the
keyboard focus cannot reach the main window with them.

<a id="notesmgr.main_window.MainWindow._bind"></a>

#### \_bind

```python
def _bind(shortcut: Shortcut, command: Callable[[], None]) -> None
```

Let every key sequence of one shortcut run a command.

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

<a id="notesmgr.main_window.MainWindow.dropped"></a>

#### dropped

```python
def dropped(item: Path, drop: Drop) -> None
```

Move what was dragged in the explorer to where it was dropped.

**Arguments**:

- `item` - The note or the folder that was dragged.
- `drop` - Where it was dropped, as the tree worked it out.

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

<a id="notesmgr.note_blocks"></a>

# notesmgr.note\_blocks

The pieces that a formatted note is drawn in, read from its HTML.

Everything about a note that has a right answer is settled here: how
deeply a piece of it is nested, what bullet or number a list item
carries, which runs of text are bold or code or a link, and how the
cells of a table line up. Drawing the note is then a matter of
writing text with tags and nothing else, and all of this is tested
without a window.

<a id="notesmgr.note_blocks.SpanStyle"></a>

## SpanStyle Objects

```python
class SpanStyle(StrEnum)
```

What is said about one run of text inside a piece of a note.

<a id="notesmgr.note_blocks.BlockKind"></a>

## BlockKind Objects

```python
class BlockKind(StrEnum)
```

What one piece of a note is, which is how it is drawn.

<a id="notesmgr.note_blocks.Span"></a>

## Span Objects

```python
class Span(NamedTuple)
```

One run of text of a piece of a note, and what is said about it.

The target is where a link leads and which file an image is in,
and is empty for a run of text that is neither of those.

<a id="notesmgr.note_blocks.Block"></a>

## Block Objects

```python
class Block(NamedTuple)
```

One piece of a note: a paragraph, a heading, a list item.

The indent is how many steps from the left the piece is written,
which is how deeply it is nested in lists and block quotes. The
prefix is the bullet or the number of a list item, and is empty
for every other kind of piece. A line across the note is a piece
holding no text at all.

<a id="notesmgr.note_blocks.HEADINGS"></a>

#### HEADINGS

The heading of each level, as the HTML of a note names them.

<a id="notesmgr.note_blocks.STYLES"></a>

#### STYLES

What each tag of the HTML says about the text inside it.

<a id="notesmgr.note_blocks.CONTAINERS"></a>

#### CONTAINERS

The tags that hold pieces of a note inside themselves.

<a id="notesmgr.note_blocks.TEXT_TAGS"></a>

#### TEXT\_TAGS

The tags that hold the text of one piece of a note.

<a id="notesmgr.note_blocks.TABLE_TAGS"></a>

#### TABLE\_TAGS

The tags of a table that say something about its cells.

<a id="notesmgr.note_blocks.CELL_TAGS"></a>

#### CELL\_TAGS

The tags that hold one cell of a table.

<a id="notesmgr.note_blocks.BULLETS"></a>

#### BULLETS

What the items of a list are marked with, by depth of nesting.

<a id="notesmgr.note_blocks.BLANKS"></a>

#### BLANKS

What is written as one blank, the line breaks of a note included.

<a id="notesmgr.note_blocks.squeezed"></a>

#### squeezed

```python
def squeezed(text: str) -> str
```

Return a run of text with every stretch of blanks made one.

The HTML of a note holds the line breaks that the note was
written with. They are blanks between words rather than breaks
to be drawn, because the panel breaks the lines where the window
is wide enough for them to be broken.

<a id="notesmgr.note_blocks.kept"></a>

#### kept

```python
def kept(spans: Sequence[Span]) -> list[Span]
```

Return the runs of text that there is anything to draw for.

<a id="notesmgr.note_blocks.trimmed"></a>

#### trimmed

```python
def trimmed(spans: Sequence[Span]) -> tuple[Span, ...]
```

Return the runs of text without the blanks at either end.

A piece of a note begins and ends with a word rather than with
the line break that the note was written with.

<a id="notesmgr.note_blocks.Container"></a>

## Container Objects

```python
@dataclass
class Container()
```

One list or block quote that is open, and how far it has come.

<a id="notesmgr.note_blocks.OpenBlock"></a>

## OpenBlock Objects

```python
@dataclass
class OpenBlock()
```

The piece of a note that is being read, as far as it is read.

<a id="notesmgr.note_blocks.OpenStyles"></a>

## OpenStyles Objects

```python
@dataclass
class OpenStyles()
```

What is said about the run of text that is being read.

<a id="notesmgr.note_blocks.TableReader"></a>

## TableReader Objects

```python
@dataclass
class TableReader()
```

The cells of a table of a note, as far as they are read.

The headings are counted rather than kept apart, because they
are the first rows of the table and the only thing that being a
heading changes is the line that is drawn under them.

<a id="notesmgr.note_blocks.TableReader.start_row"></a>

#### start\_row

```python
def start_row() -> None
```

Begin another row of the table.

<a id="notesmgr.note_blocks.TableReader.start_cell"></a>

#### start\_cell

```python
def start_cell(style: str, heading: bool) -> None
```

Begin another cell of the row that is being read.

**Arguments**:

- `style` - The style attribute of the cell, which is where
  the markdown table said how the column lines up.
- `heading` - Whether the cell is a heading of its column.

<a id="notesmgr.note_blocks.TableReader.add_text"></a>

#### add\_text

```python
def add_text(text: str) -> None
```

Take a run of text that belongs to the cell being read.

<a id="notesmgr.note_blocks.TableReader.end_cell"></a>

#### end\_cell

```python
def end_cell() -> None
```

Put the cell that was read at the end of its row.

<a id="notesmgr.note_blocks.TableReader.text"></a>

#### text

```python
def text() -> str
```

Return the table written in columns of monospaced text.

<a id="notesmgr.note_blocks.item_prefix"></a>

#### item\_prefix

```python
def item_prefix(containers: Sequence[Container]) -> str
```

Return the bullet or the number that a list item carries.

An ordered list numbers its items as it goes, and an unordered
one marks them with a bullet that says how deeply the list is
nested, so that a nested list is told from the one holding it
even where the indentation is easy to miss.

<a id="notesmgr.note_blocks.NoteParser"></a>

## NoteParser Objects

```python
class NoteParser(HTMLParser)
```

Reads the HTML of a note into the pieces that it is drawn in.

<a id="notesmgr.note_blocks.NoteParser.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Get ready to read HTML, no piece of it having been read.

<a id="notesmgr.note_blocks.NoteParser.note_blocks"></a>

#### note\_blocks

```python
def note_blocks() -> tuple[Block, ...]
```

Return the pieces of the note, all of it having been read.

<a id="notesmgr.note_blocks.NoteParser.handle_starttag"></a>

#### handle\_starttag

```python
def handle_starttag(tag: str, attrs: list[tuple[str, Optional[str]]]) -> None
```

Begin what a tag begins, ignoring one that begins nothing.

<a id="notesmgr.note_blocks.NoteParser.handle_endtag"></a>

#### handle\_endtag

```python
def handle_endtag(tag: str) -> None
```

End what a tag ends, ignoring one that ends nothing.

<a id="notesmgr.note_blocks.NoteParser.handle_data"></a>

#### handle\_data

```python
def handle_data(data: str) -> None
```

Take a run of text of whatever is being read.

<a id="notesmgr.note_blocks.NoteParser._open_other"></a>

#### \_open\_other

```python
def _open_other(tag: str, attrs: Mapping[str, Optional[str]]) -> None
```

Begin one of the tags that stands on its own.

<a id="notesmgr.note_blocks.NoteParser._depth"></a>

#### \_depth

```python
def _depth() -> int
```

Return how many lists and quotes what is read is inside.

<a id="notesmgr.note_blocks.NoteParser._text_kind"></a>

#### \_text\_kind

```python
def _text_kind() -> BlockKind
```

Return whether text now read is quoted or an ordinary piece.

<a id="notesmgr.note_blocks.NoteParser._open_block"></a>

#### \_open\_block

```python
def _open_block(kind: BlockKind) -> None
```

Begin another piece of the note, at the depth it is read at.

<a id="notesmgr.note_blocks.NoteParser._block_spans"></a>

#### \_block\_spans

```python
def _block_spans() -> tuple[Span, ...]
```

Return the runs of text of the piece that was read.

The text of a code block is kept exactly as it is written,
while a paragraph loses the blanks at either end of it.

<a id="notesmgr.note_blocks.NoteParser._flush"></a>

#### \_flush

```python
def _flush() -> None
```

Put the piece that was read among the pieces of the note.

<a id="notesmgr.note_blocks.NoteParser._open_container"></a>

#### \_open\_container

```python
def _open_container(tag: str) -> None
```

Begin a list or a block quote, which holds pieces of its own.

<a id="notesmgr.note_blocks.NoteParser._close_container"></a>

#### \_close\_container

```python
def _close_container() -> None
```

End a list or a block quote, ignoring an end of neither.

<a id="notesmgr.note_blocks.NoteParser._open_item"></a>

#### \_open\_item

```python
def _open_item() -> None
```

Begin a list item, with the bullet or the number it carries.

<a id="notesmgr.note_blocks.NoteParser._open_code"></a>

#### \_open\_code

```python
def _open_code() -> None
```

Begin a code block, whose text is taken as it is written.

<a id="notesmgr.note_blocks.NoteParser._close_code"></a>

#### \_close\_code

```python
def _close_code() -> None
```

Put a code block among the pieces, without its indentation.

A code block that is nested is written indented in the note,
and that indentation is taken off so that the code stands
where the piece holding it stands.

<a id="notesmgr.note_blocks.NoteParser._open_style"></a>

#### \_open\_style

```python
def _open_style(style: SpanStyle) -> None
```

Begin what is said about the run of text that follows.

Inside a code block nothing is said about the text, because
the tags of the HTML are the text of the note there.

<a id="notesmgr.note_blocks.NoteParser._close_style"></a>

#### \_close\_style

```python
def _close_style(style: SpanStyle) -> None
```

End what was said, ignoring an end of what was not said.

<a id="notesmgr.note_blocks.NoteParser._open_link"></a>

#### \_open\_link

```python
def _open_link(target: str) -> None
```

Begin a link, whose text is drawn as leading somewhere.

<a id="notesmgr.note_blocks.NoteParser._close_link"></a>

#### \_close\_link

```python
def _close_link() -> None
```

End a link, so that what follows is ordinary text again.

<a id="notesmgr.note_blocks.NoteParser._add_text"></a>

#### \_add\_text

```python
def _add_text(text: str) -> None
```

Take a run of text of the piece being read, if one is open.

<a id="notesmgr.note_blocks.NoteParser._read"></a>

#### \_read

```python
def _read(text: str) -> str
```

Return a run of text as it belongs in the piece being read.

Inside a code block the text is what the note holds, and
everywhere else every stretch of blanks is one blank. The
blanks after a line break that the note asked for are
dropped, because the next line begins with its first word.

<a id="notesmgr.note_blocks.NoteParser._after_break"></a>

#### \_after\_break

```python
def _after_break() -> bool
```

Return whether a line break was the last thing read.

<a id="notesmgr.note_blocks.NoteParser._span"></a>

#### \_span

```python
def _span(text: str, target: str = '') -> Span
```

Return a run of text with what is said about it now.

<a id="notesmgr.note_blocks.NoteParser._add_break"></a>

#### \_add\_break

```python
def _add_break() -> None
```

Take a line break that the note asks to have drawn.

<a id="notesmgr.note_blocks.NoteParser._add_image"></a>

#### \_add\_image

```python
def _add_image(attrs: Mapping[str, Optional[str]]) -> None
```

Take an image of the note as a run of text of its own.

<a id="notesmgr.note_blocks.NoteParser._add_rule"></a>

#### \_add\_rule

```python
def _add_rule() -> None
```

Put a line across the note among the pieces of it.

<a id="notesmgr.note_blocks.NoteParser._open_table_tag"></a>

#### \_open\_table\_tag

```python
def _open_table_tag(tag: str, attrs: Mapping[str, Optional[str]]) -> None
```

Begin a table, a row of it, or a cell of a row of it.

<a id="notesmgr.note_blocks.NoteParser._close_table_tag"></a>

#### \_close\_table\_tag

```python
def _close_table_tag(tag: str) -> None
```

End a table or a cell of it, a row needing no ending.

<a id="notesmgr.note_blocks.NoteParser._open_table"></a>

#### \_open\_table

```python
def _open_table() -> None
```

Begin a table, which is read on its own and drawn as text.

<a id="notesmgr.note_blocks.NoteParser._close_table"></a>

#### \_close\_table

```python
def _close_table() -> None
```

Put the table that was read among the pieces of the note.

<a id="notesmgr.note_blocks.html_blocks"></a>

#### html\_blocks

```python
def html_blocks(html: str) -> tuple[Block, ...]
```

Return the pieces that the HTML of a note is drawn in.

**Arguments**:

- `html` - The HTML of the note, as the markdown of it gave.
  

**Returns**:

  Every piece of the note, in the order it is drawn in.

<a id="notesmgr.note_blocks.markdown_blocks"></a>

#### markdown\_blocks

```python
def markdown_blocks(text: str) -> tuple[Block, ...]
```

Return the pieces that a note written in markdown is drawn in.

**Arguments**:

- `text` - The markdown of the note, as much of it as is shown.
  

**Returns**:

  Every piece of the note, in the order it is drawn in.

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

<a id="notesmgr.explorer_drop"></a>

# notesmgr.explorer\_drop

Where a note or a folder lands when it is dropped in the tree.

<a id="notesmgr.explorer_drop.Drop"></a>

## Drop Objects

```python
class Drop(NamedTuple)
```

Where a dragged item lands: a folder, and a place in it.

A note lands at a place among the notes of the folder, counted
as the notes stand before it is moved. A folder lands in the
folder itself and at no place in it, because the folders of a
folder are shown in alphabetical order rather than in an order
of their own, which is what a place of None says.

The place is called so rather than an index, because a tuple
numbers what it holds through a method of that name already.

<a id="notesmgr.explorer_drop.folder_drop"></a>

#### folder\_drop

```python
def folder_drop(project: Project, dragged: Path, over: Path) -> Optional[Drop]
```

Return where a dragged folder lands, None when it cannot land.

A folder goes into a folder of the project and nowhere else. It
goes neither into itself nor into a folder of its own, which
would take it out of the project altogether, and the root folder
of the project is the project itself and does not move.

**Arguments**:

- `project` - The project as the tree is showing it.
- `dragged` - The folder that is being dragged.
- `over` - The item of the tree that the pointer is over.
  

**Returns**:

  The folder it lands in, None when it lands nowhere.

<a id="notesmgr.explorer_drop.note_place"></a>

#### note\_place

```python
def note_place(project: Project, over: Path,
               lower: bool) -> Optional[tuple[Folder, int]]
```

Return the folder and the place in it that an item stands for.

The upper half of a note is the place of that note and the lower
half the place after it, a folder is the place after its last
note, and the lower half of a template is the place of the first
note of its folder. The upper half of a template is above every
note of the folder, where no note can go.

**Arguments**:

- `project` - The project as the tree is showing it.
- `over` - The item of the tree that the pointer is over.
- `lower` - Whether the pointer is in the lower half of that item.
  

**Returns**:

  The folder the note lands in and the place it lands at, None
  when the item stands for no place at all.

<a id="notesmgr.explorer_drop.stays_put"></a>

#### stays\_put

```python
def stays_put(holder: Folder, dragged: Path, index: int) -> bool
```

Return whether a place is where a note is standing already.

A note dropped upon itself, and a note dropped where it would
land between the notes it is already between, has not moved, so
there is nothing to do and nothing to show either.

**Arguments**:

- `holder` - The folder that the note would land in.
- `dragged` - The note that is being dragged.
- `index` - The place it would land at.
  

**Returns**:

  Whether the note is at that place already.

<a id="notesmgr.explorer_drop.dragged_note"></a>

#### dragged\_note

```python
def dragged_note(project: Project, dragged: Path) -> bool
```

Return whether an item of the tree is a note that can be dragged.

The tree is asked rather than the name, so that the template of a
folder, which is no note of the order of that folder, and a row
that another program has taken away under the tree, are both left
where they are.

**Arguments**:

- `project` - The project as the tree is showing it.
- `dragged` - The item that is being dragged.
  

**Returns**:

  Whether the project holds it as a note of one of its folders.

<a id="notesmgr.explorer_drop.note_drop"></a>

#### note\_drop

```python
def note_drop(project: Project, dragged: Path, over: Path,
              lower: bool) -> Optional[Drop]
```

Return where a dragged note lands, None when it cannot land.

**Arguments**:

- `project` - The project as the tree is showing it.
- `dragged` - The note that is being dragged.
- `over` - The item of the tree that the pointer is over.
- `lower` - Whether the pointer is in the lower half of that item.
  

**Returns**:

  The folder and the place it lands at, None for nowhere.

<a id="notesmgr.explorer_drop.drop_target"></a>

#### drop\_target

```python
def drop_target(project: Project, dragged: Path, over: Optional[Path],
                lower: bool) -> Optional[Drop]
```

Return where what is dragged lands, None when it cannot land.

A note and a folder of the project are dragged, and everything
else the tree shows stays where it is: every folder has one
template, and it is no note of the order of that folder.

**Arguments**:

- `project` - The project as the tree is showing it.
- `dragged` - The item that is being dragged.
- `over` - The item of the tree that the pointer is over, None
  when the pointer is over no item of it at all.
- `lower` - Whether the pointer is in the lower half of that item.
  

**Returns**:

  Where it lands, None when it lands nowhere.

<a id="notesmgr.explorer_drop.drop_item"></a>

#### drop\_item

```python
def drop_item(item: Path, drop: Drop) -> Path
```

Move a note or a folder to where it was dropped.

**Arguments**:

- `item` - The note or the folder that was dragged.
- `drop` - Where it was dropped, as the tree worked it out.
  

**Returns**:

  The note or the folder where it now is.
  

**Raises**:

- `NotesmgrError` - The move cannot be made, which the message of
  the error says why.

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

<a id="notesmgr.note_ops.NOT_MOVED"></a>

#### NOT\_MOVED

What is said about a note that could not be moved to a folder.

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

<a id="notesmgr.note_ops.moved_to"></a>

#### moved\_to

```python
def moved_to(names: Sequence[str], name: str, index: int) -> list[str]
```

Return an order with one of its notes put at a place in it.

The place is where the note lands among the notes as they stand
now, so that a note dropped upon the note at a place takes that
place, and a note dropped below the last note comes last.

**Arguments**:

- `names` - The notes of a folder, in the order they are shown in.
- `name` - The note to put there, which may be none of them.
- `index` - The place it lands at, kept within the folder.
  

**Returns**:

  The order as it is after the move.

<a id="notesmgr.note_ops.reordered"></a>

#### reordered

```python
def reordered(folder: Path, order: Sequence[str],
              moved: Sequence[str]) -> None
```

Write the order of a folder, when a move changed the order.

**Arguments**:

- `folder` - The folder whose notes were moved.
- `order` - The order the folder had.
- `moved` - The order it has after the move.
  

**Raises**:

- `NotesmgrError` - The order file cannot be written.

<a id="notesmgr.note_ops.shift_note"></a>

#### shift\_note

```python
def shift_note(note: Path, offset: int) -> Path
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

<a id="notesmgr.note_ops.place_note"></a>

#### place\_note

```python
def place_note(folder: Path, name: str, index: int) -> None
```

Put one of the notes of a folder at a place in its order.

**Arguments**:

- `folder` - The folder that the note is in.
- `name` - The name of the note that is put there.
- `index` - The place it lands at, among the notes as they stand.
  

**Raises**:

- `NotesmgrError` - The folder or its order file cannot be read,
  or the order file cannot be written.

<a id="notesmgr.note_ops.move_note"></a>

#### move\_note

```python
def move_note(note: Path, folder: Path, index: int) -> Path
```

Move a note to a place among the notes of a folder.

The folder is the note's own folder when the note is only put at
another place in it, and another folder of the project when it is
moved there, which leaves the order of both folders in order.

**Arguments**:

- `note` - The note to move.
- `folder` - The folder it is to be in.
- `index` - The place it lands at, among the notes of that folder
  as they stand now.
  

**Returns**:

  The note where it now is.
  

**Raises**:

- `NotesmgrError` - The folder holds a file of that name already,
  the note cannot be moved, or a note order cannot be read
  or written.

<a id="notesmgr.clipboard_linux"></a>

# notesmgr.clipboard\_linux

Putting a formatted copy of a note on the clipboard of a desktop.

<a id="notesmgr.clipboard_linux.XCLIP"></a>

#### XCLIP

What puts HTML on the clipboard of an X11 desktop.

<a id="notesmgr.clipboard_linux.WL_COPY"></a>

#### WL\_COPY

What puts HTML on the clipboard of a Wayland desktop.

<a id="notesmgr.clipboard_linux.TOOLS"></a>

#### TOOLS

The programs that can take a formatted copy, the first one first.

A Wayland desktop usually answers for X11 programs as well, so the
one that works on both is the one that is tried first.

<a id="notesmgr.clipboard_linux.NO_TOOL"></a>

#### NO\_TOOL

What is said when the desktop has neither of the two programs.

<a id="notesmgr.clipboard_linux.CHARSET"></a>

#### CHARSET

What says that the HTML of a copy is written as UTF-8.

<a id="notesmgr.clipboard_linux.html_tool"></a>

#### html\_tool

```python
def html_tool() -> Optional[Sequence[str]]
```

Return the program that takes a formatted copy, None for none.

<a id="notesmgr.clipboard_linux.copy_to_clipboard"></a>

#### copy\_to\_clipboard

```python
def copy_to_clipboard(payload: RichText) -> None
```

Put a formatted copy of a note on the clipboard of a desktop.

The clipboard of X11 and of Wayland is owned by a program rather
than held by the system, and the program that owns it offers the
one shape it was given, so the formatted shape is what is put
there. That program goes on running to answer for the clipboard,
and is therefore not waited for.

**Arguments**:

- `payload` - The copy to put there.
  

**Raises**:

- `NotesmgrError` - The desktop has no program that takes a
  formatted copy, or the one it has refused this copy.

<a id="notesmgr.clipboard_windows"></a>

# notesmgr.clipboard\_windows

Putting a formatted copy of a note on the clipboard of Windows.

<a id="notesmgr.clipboard_windows.HEADER"></a>

#### HEADER

What says where the pieces of an HTML Format payload begin and end.

Every number is a count of bytes from the very start of the payload,
written with as many digits as it can ever need, so that filling the
numbers in does not move what they point at.

<a id="notesmgr.clipboard_windows.OPENING"></a>

#### OPENING

What stands before the piece of the payload that is pasted.

<a id="notesmgr.clipboard_windows.CLOSING"></a>

#### CLOSING

What stands after the piece of the payload that is pasted.

<a id="notesmgr.clipboard_windows.HTML_FORMAT"></a>

#### HTML\_FORMAT

What the clipboard of Windows calls the shape that keeps markup.

<a id="notesmgr.clipboard_windows.UNICODE_TEXT"></a>

#### UNICODE\_TEXT

What the clipboard of Windows calls plain text, as CF_UNICODETEXT.

<a id="notesmgr.clipboard_windows.MOVEABLE"></a>

#### MOVEABLE

How memory that is handed over to the clipboard is allocated.

<a id="notesmgr.clipboard_windows.NOT_WINDOWS"></a>

#### NOT\_WINDOWS

What is said when the clipboard of Windows is asked for elsewhere.

<a id="notesmgr.clipboard_windows.NOT_OPENED"></a>

#### NOT\_OPENED

What is said when the clipboard could not be opened at all.

<a id="notesmgr.clipboard_windows.NO_MEMORY"></a>

#### NO\_MEMORY

What is said when the memory for a copy could not be had.

<a id="notesmgr.clipboard_windows.byte_length"></a>

#### byte\_length

```python
def byte_length(text: str) -> int
```

Return how many bytes a text is when it is written as UTF-8.

<a id="notesmgr.clipboard_windows.cf_html"></a>

#### cf\_html

```python
def cf_html(fragment: str) -> str
```

Return the HTML Format payload that Windows takes a copy in.

The header says where the document begins and ends and where the
piece of it that is pasted begins and ends. All four are counted
in bytes rather than in characters, so a note holding anything
but plain ASCII is counted as the UTF-8 that it is written as.

**Arguments**:

- `fragment` - The HTML of the note, as it goes inside a body.
  

**Returns**:

  The payload, header and document together.

<a id="notesmgr.clipboard_windows.html_bytes"></a>

#### html\_bytes

```python
def html_bytes(fragment: str) -> bytes
```

Return the formatted shape of a copy as Windows holds it.

<a id="notesmgr.clipboard_windows.text_bytes"></a>

#### text\_bytes

```python
def text_bytes(text: str) -> bytes
```

Return the plain shape of a copy as Windows holds it.

<a id="notesmgr.clipboard_windows.moveable_memory"></a>

#### moveable\_memory

```python
def moveable_memory(kernel32: ctypes.CDLL, data: bytes) -> int
```

Return a handle to memory holding the given bytes.

The clipboard takes over the memory it is given, so what is
allocated here is moveable, as the clipboard asks, and is not
freed again by notesmgr.

**Arguments**:

- `kernel32` - The library of Windows that hands out memory.
- `data` - What the memory is to hold.
  

**Returns**:

  The handle to give to the clipboard.
  

**Raises**:

- `NotesmgrError` - The memory could not be had.

<a id="notesmgr.clipboard_windows.write_clipboard"></a>

#### write\_clipboard

```python
def write_clipboard(user32: ctypes.CDLL, kernel32: ctypes.CDLL,
                    shapes: Sequence[tuple[int, bytes]]) -> None
```

Put every shape of one copy on the clipboard in one session.

The clipboard is emptied once and then filled with every shape,
because opening it a second time would take away what the first
session put there.

**Arguments**:

- `user32` - The library of Windows that owns the clipboard.
- `kernel32` - The library of Windows that hands out memory.
- `shapes` - What each shape of the copy is called and holds.
  

**Raises**:

- `NotesmgrError` - The clipboard could not be opened, or the
  memory for a shape could not be had.

<a id="notesmgr.clipboard_windows.copy_to_clipboard"></a>

#### copy\_to\_clipboard

```python
def copy_to_clipboard(payload: RichText) -> None
```

Put a formatted copy of a note on the clipboard of Windows.

**Arguments**:

- `payload` - The copy to put there.
  

**Raises**:

- `NotesmgrError` - This is no Windows, or Windows did not take
  the copy.

<a id="notesmgr.rich_clipboard"></a>

# notesmgr.rich\_clipboard

The formatted copy of a note, and where each platform puts it.

<a id="notesmgr.rich_clipboard.PLAIN"></a>

#### PLAIN

How a note that is no markdown is written for a formatted copy.

Such a note is shown in the fixed width font and exactly as it is
written, so the copy of it keeps its own line breaks and the columns
of a table that was lined up by hand.

<a id="notesmgr.rich_clipboard.IMAGE_SOURCE"></a>

#### IMAGE\_SOURCE

What names the file of an image in the HTML of a note.

<a id="notesmgr.rich_clipboard.BACKENDS"></a>

#### BACKENDS

What puts a formatted copy on the clipboard of each platform.

Every other platform is taken to be a desktop of X11 or of Wayland,
which is what Linux and the BSDs have.

<a id="notesmgr.rich_clipboard.absolute_source"></a>

#### absolute\_source

```python
def absolute_source(folder: Optional[Path], match: re.Match[str]) -> str
```

Return one image of a note naming its file wherever it is read.

A copy is pasted somewhere else than into the folder of the note,
so an image that the note names beside itself is named by its
whole path instead. An image that is on the network, or that
names no file that can be found from where the note stands, is
left exactly as the note wrote it.

**Arguments**:

- `folder` - The folder that holds the note, None when the note
  is copied from nowhere in particular.
- `match` - The image of the HTML that is being named again.
  

**Returns**:

  The image as the copy of the note is to hold it.

<a id="notesmgr.rich_clipboard.local_images"></a>

#### local\_images

```python
def local_images(html: str, folder: Optional[Path]) -> str
```

Return HTML in which every image beside the note names its file.

<a id="notesmgr.rich_clipboard.note_fragment"></a>

#### note\_fragment

```python
def note_fragment(text: str,
                  markdown: bool,
                  folder: Optional[Path] = None) -> str
```

Return the HTML that a formatted copy of a note is made of.

**Arguments**:

- `text` - The note, as much of it as is shown.
- `markdown` - Whether the note is written in markdown, and is
  therefore formatted rather than kept as it is written.
- `folder` - The folder that holds the note, which is what an
  image that the note shows is named from.
  

**Returns**:

  The HTML of the note, as it goes inside a body.

<a id="notesmgr.rich_clipboard.note_rich_text"></a>

#### note\_rich\_text

```python
def note_rich_text(text: str,
                   markdown: bool,
                   folder: Optional[Path] = None) -> RichText
```

Return a copy of a note in the shapes a clipboard takes it in.

<a id="notesmgr.rich_clipboard.backend"></a>

#### backend

```python
def backend() -> Callable[[RichText], None]
```

Return what puts a formatted copy on the clipboard here.

<a id="notesmgr.rich_clipboard.copy_rich"></a>

#### copy\_rich

```python
def copy_rich(payload: RichText) -> None
```

Put a formatted copy of a note on the clipboard of the system.

**Arguments**:

- `payload` - The copy to put there.
  

**Raises**:

- `NotesmgrError` - The system has no way of taking a formatted
  copy, or the way it has did not take this one.

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

A button that is described with no command has nothing to do,
and is greyed out whatever is selected, so that a row can be
the whole row before every one of its buttons is wired up.

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

A button that was described with no command has nothing to do
when pressed, and stays greyed out however much the selection
would allow it.

**Arguments**:

- `labels` - What the buttons that can be used now say.

<a id="notesmgr.note_tags"></a>

# notesmgr.note\_tags

The text tags that the pieces of a formatted note are drawn with.

<a id="notesmgr.note_tags.CODE_BACKGROUND"></a>

#### CODE\_BACKGROUND

Colour behind code, which is what sets it off from the prose.

<a id="notesmgr.note_tags.QUOTE_COLOUR"></a>

#### QUOTE\_COLOUR

Colour of a quoted piece, a grey that is read as quieter text.

<a id="notesmgr.note_tags.LINK_COLOUR"></a>

#### LINK\_COLOUR

Colour of the text of a link, the blue that a link is known by.

<a id="notesmgr.note_tags.RULE_COLOUR"></a>

#### RULE\_COLOUR

Colour of a line drawn across the note.

<a id="notesmgr.note_tags.LINK_TAG"></a>

#### LINK\_TAG

Tag of the text of a link, which is underlined and coloured.

<a id="notesmgr.note_tags.CODE_SPAN_TAG"></a>

#### CODE\_SPAN\_TAG

Tag of code inside a line of prose, which is set off behind.

<a id="notesmgr.note_tags.STRIKE_TAG"></a>

#### STRIKE\_TAG

Tag of text that is struck through, which Tk draws a line over.

<a id="notesmgr.note_tags.IMAGE_TAG"></a>

#### IMAGE\_TAG

Tag of an image that is named rather than drawn.

<a id="notesmgr.note_tags.GAP_TAG"></a>

#### GAP\_TAG

Tag of the blank line that is left between two pieces of a note.

<a id="notesmgr.note_tags.INDENT_TAG"></a>

#### INDENT\_TAG

Tag that writes a piece of a note so many steps from the left.

<a id="notesmgr.note_tags.ITEM_TAG"></a>

#### ITEM\_TAG

Tag that writes a list item, its bullet standing out to the left.

What the bullet takes up is left free on the lines after the first
one, so that a list item that is broken over several lines reads as
one item rather than as the beginning of another.

<a id="notesmgr.note_tags.MAX_INDENT"></a>

#### MAX\_INDENT

Most steps from the left that a piece of a note is written at.

A note nested deeper than this is written at this depth, which
keeps a note that is nothing but nested lists readable in a narrow
window.

<a id="notesmgr.note_tags.RAW_KEY"></a>

#### RAW\_KEY

The font of a note that is shown as it is written.

A note that is no markdown is shown as the file holds it, so it is
drawn with one width per letter, which is what keeps a table that
was lined up by hand lined up. It is the font of the area itself
rather than of a tag, so that it follows the size of the note the
way every other font of it does.

<a id="notesmgr.note_tags.GAP_KEY"></a>

#### GAP\_KEY

The font of the blank line that is left between two pieces.

A blank line is as tall as the font of it, which is how the room
between two pieces of a note is left. Tk would space the lines
inside a code block and a table as well.

<a id="notesmgr.note_tags.HEADING_GAPS"></a>

#### HEADING\_GAPS

Blank lines above a heading, which is what sets a part apart.

<a id="notesmgr.note_tags.BULLET_ROOM"></a>

#### BULLET\_ROOM

What a bullet is taken to take up on the line that carries it.

<a id="notesmgr.note_tags.indent_tag"></a>

#### indent\_tag

```python
def indent_tag(block: Block) -> str
```

Return the tag that writes a piece of a note where it belongs.

**Arguments**:

- `block` - The piece of the note that is to be written.
  

**Returns**:

  The name of the tag that indents it, which leaves room for
  the bullet of a list item and none for anything else.

<a id="notesmgr.note_tags.gap_lines"></a>

#### gap\_lines

```python
def gap_lines(block: Block, previous: Optional[Block]) -> int
```

Return how many blank lines are left above a piece of a note.

A heading is set off from the part above it by a wider gap, and
the items of one list follow one another with no gap at all, the
way the note was written. Nothing is left above the first piece
of a note, which begins at the top of the area.

**Arguments**:

- `block` - The piece of the note that is to be written.
- `previous` - The piece written above it, None for the first one.
  

**Returns**:

  How many blank lines to write above it.

<a id="notesmgr.note_tags.span_styles"></a>

#### span\_styles

```python
def span_styles(span: Span) -> tuple[str, ...]
```

Return the tags that say how one run of text looks.

The font of a run of text is a tag of its own, and these are
what is drawn on top of it: the colour of a link, the shading
of code inside a line of prose, the line over text that is
struck through, and how an image is named.

<a id="notesmgr.note_tags.NoteTags"></a>

## NoteTags Objects

```python
class NoteTags()
```

Defines and hands out the tags that a note is drawn with.

The tag that carries a font is made the first time a note needs
it, and every tag that is measured in pixels is given afresh
whenever the note is drawn in another size, so that the space
between the pieces and the indentation of a list follow the text.

<a id="notesmgr.note_tags.NoteTags.__init__"></a>

#### \_\_init\_\_

```python
def __init__(area: tkinter.Text, size: Optional[int] = None) -> None
```

Define the tags of a text area that a note is drawn in.

**Arguments**:

- `area` - The text area that the tags belong to.
- `size` - The size to draw the ordinary text of a note in,
  None for the size that Tk draws text in.

<a id="notesmgr.note_tags.NoteTags._colour_tags"></a>

#### \_colour\_tags

```python
def _colour_tags() -> None
```

Define the tags that say nothing about how large the text is.

<a id="notesmgr.note_tags.NoteTags._sized_tags"></a>

#### \_sized\_tags

```python
def _sized_tags() -> None
```

Define the tags that are measured in the size drawn in.

The room between two pieces of a note is left by the blank
line between them, and the indentation of a list is measured
in what the text of the note takes up, so both of them are
given again whenever the note is drawn in another size.

<a id="notesmgr.note_tags.NoteTags.font_tag_of"></a>

#### font\_tag\_of

```python
def font_tag_of(kind: BlockKind, span: Span) -> str
```

Return the tag that draws a run of text in its own font.

The tag is defined the first time a note needs it, and from
then on it follows the size that the note is drawn in,
because it is the font itself that the size is changed on.

**Arguments**:

- `kind` - What the piece of the note holding the run of text is.
- `span` - The run of text that is to be drawn.
  

**Returns**:

  The name of the tag that carries its font.

<a id="notesmgr.note_tags.NoteTags.span_tags"></a>

#### span\_tags

```python
def span_tags(kind: BlockKind, span: Span, indent: str) -> tuple[str, ...]
```

Return every tag that one run of text of a piece is drawn with.

**Arguments**:

- `kind` - What the piece of the note holding the run of text is.
- `span` - The run of text that is to be drawn.
- `indent` - The tag that writes the piece where it belongs.
  

**Returns**:

  The tags to give the text, the piece it belongs to first
  and what is said about the run of text itself last.

<a id="notesmgr.note_tags.NoteTags.resize"></a>

#### resize

```python
def resize(size: int) -> int
```

Draw the note in another size from now on.

<a id="notesmgr.note_tags.NoteTags.zoom"></a>

#### zoom

```python
def zoom(step: int) -> int
```

Draw so many steps larger, or smaller for a step below zero.

<a id="notesmgr.note_tags.NoteTags.normal_size"></a>

#### normal\_size

```python
def normal_size() -> int
```

Draw the note in the size that it started out in.

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

<a id="notesmgr.note_table"></a>

# notesmgr.note\_table

Laying a table of a note out in columns of monospaced text.

<a id="notesmgr.note_table.MAX_COLUMN"></a>

#### MAX\_COLUMN

Most characters that one column of a table is made wide.

A cell holding more than this is written over several lines instead
of making the table wider than the panel can show.

<a id="notesmgr.note_table.CELL_GAP"></a>

#### CELL\_GAP

What is written between two cells of the same row.

<a id="notesmgr.note_table.RULE_GAP"></a>

#### RULE\_GAP

What is written between two cells of the line under the headings.

<a id="notesmgr.note_table.RULE_CHAR"></a>

#### RULE\_CHAR

What the line under the headings of a table is drawn with.

<a id="notesmgr.note_table.Align"></a>

## Align Objects

```python
class Align(StrEnum)
```

Which side of its column the text of a cell is written against.

<a id="notesmgr.note_table.cell_align"></a>

#### cell\_align

```python
def cell_align(style: str) -> Align
```

Return the alignment that the style of a cell asks for.

**Arguments**:

- `style` - The style attribute of a cell of the HTML of a note,
  empty for a cell that carries none.
  

**Returns**:

  What the text-align of the style says, and LEFT when it says
  nothing, which is what a markdown table without colons means.

<a id="notesmgr.note_table.squared"></a>

#### squared

```python
def squared(rows: Sequence[Sequence[str]], columns: int) -> list[list[str]]
```

Return the rows with every one of them holding every column.

A markdown table is allowed to leave the cells at the end of a
row out, and every row holding every column is what lets the
rest of the laying out be written without asking each time.

<a id="notesmgr.note_table.every_align"></a>

#### every\_align

```python
def every_align(aligns: Sequence[Align], columns: int) -> list[Align]
```

Return an alignment for every column, LEFT for the unsaid ones.

<a id="notesmgr.note_table.column_width"></a>

#### column\_width

```python
def column_width(rows: Sequence[Sequence[str]], index: int) -> int
```

Return how wide one column of a table is made.

A column is as wide as its widest cell, up to the most a column
may be, and one character wide when all of its cells are empty,
so that the line under the headings is drawn for it as well.

<a id="notesmgr.note_table.wrapped_cell"></a>

#### wrapped\_cell

```python
def wrapped_cell(text: str, width: int) -> list[str]
```

Return the lines that a cell takes up in a column of a width.

<a id="notesmgr.note_table.line_at"></a>

#### line\_at

```python
def line_at(lines: Sequence[str], number: int) -> str
```

Return one line of a wrapped cell, empty past its last line.

<a id="notesmgr.note_table.padded_cell"></a>

#### padded\_cell

```python
def padded_cell(text: str, width: int, align: Align) -> str
```

Return the text of a cell written against its side of a column.

<a id="notesmgr.note_table.row_lines"></a>

#### row\_lines

```python
def row_lines(row: Sequence[str], widths: Sequence[int],
              aligns: Sequence[Align]) -> list[str]
```

Return the lines that one row of a table takes up.

A row is as tall as the cell of it that takes the most lines,
and the cells that take fewer are left blank underneath.

<a id="notesmgr.note_table.rule_line"></a>

#### rule\_line

```python
def rule_line(widths: Sequence[int]) -> str
```

Return the line that is drawn under the headings of a table.

<a id="notesmgr.note_table.table_text"></a>

#### table\_text

```python
def table_text(rows: Sequence[Sequence[str]],
               aligns: Sequence[Align],
               headings: int = 0) -> str
```

Return a table written in columns of monospaced text.

**Arguments**:

- `rows` - The cells of each row, where a row is allowed to hold
  fewer cells than the widest row of the table does.
- `aligns` - Which side of its column each column is written
  against, as far as the table said.
- `headings` - How many rows at the top of the table are heading
  rows, which is what the line across it is drawn under.
  

**Returns**:

  The lines of the table, and nothing at all for a table that
  holds no cells to write.

<a id="notesmgr.note_fonts"></a>

# notesmgr.note\_fonts

The fonts that a note is drawn with, and how large they are.

<a id="notesmgr.note_fonts.MIN_SIZE"></a>

#### MIN\_SIZE

Smallest size that a note is drawn in, however small it is asked.

<a id="notesmgr.note_fonts.MAX_SIZE"></a>

#### MAX\_SIZE

Largest size that a note is drawn in, however large it is asked.

<a id="notesmgr.note_fonts.FALLBACK_SIZE"></a>

#### FALLBACK\_SIZE

Size used where Tk names no size for the text that it draws.

<a id="notesmgr.note_fonts.TEXT_FONT"></a>

#### TEXT\_FONT

The font that Tk draws ordinary text with on this system.

<a id="notesmgr.note_fonts.FIXED_FONT"></a>

#### FIXED\_FONT

The font that Tk draws text of one width per letter with.

<a id="notesmgr.note_fonts.BODY_SCALE"></a>

#### BODY\_SCALE

How large the ordinary text of a note is drawn, which is as given.

<a id="notesmgr.note_fonts.FIXED_KINDS"></a>

#### FIXED\_KINDS

The pieces of a note that are drawn with one width per letter.

Code is written in such a font to be read in one, a table is lined
up in columns that only such a font keeps lined up, and a line
across the note is a row of letters that only such a font joins.

<a id="notesmgr.note_fonts.HEADING_SCALES"></a>

#### HEADING\_SCALES

How much larger than the text of a note each heading is drawn.

<a id="notesmgr.note_fonts.note_size"></a>

#### note\_size

```python
def note_size(size: int) -> int
```

Return a size that a note can be read at.

**Arguments**:

- `size` - The size that is asked for, from wherever it came.
  

**Returns**:

  That size, kept within what can be read, so that holding a
  key down can neither make a note vanish nor fill the window
  with a single word.

<a id="notesmgr.note_fonts.default_size"></a>

#### default\_size

```python
def default_size(widget: tkinter.Misc) -> int
```

Return the size that Tk draws ordinary text in on this system.

Tk gives a size in points, or in pixels written as a negative
number, and either way how large it is, is where a note starts.

<a id="notesmgr.note_fonts.family_of"></a>

#### family\_of

```python
def family_of(name: str, widget: tkinter.Misc) -> str
```

Return the family of one of the fonts that Tk names itself.

<a id="notesmgr.note_fonts.FontKey"></a>

## FontKey Objects

```python
class FontKey(NamedTuple)
```

What tells one of the fonts that a note is drawn with from another.

The scale is how large the font is against the size that the
note is drawn in, so that making the note larger or smaller is
one size that every font of it follows.

<a id="notesmgr.note_fonts.BODY_KEY"></a>

#### BODY\_KEY

The font that the ordinary text of a note is drawn with.

<a id="notesmgr.note_fonts.font_key"></a>

#### font\_key

```python
def font_key(
    kind: BlockKind, styles: AbstractSet[SpanStyle] = frozenset()) -> FontKey
```

Return the font that one run of text of a piece is drawn with.

A heading is drawn larger and bold, a quote in italics, and
code and a table in the font of one width per letter. What is
said about the run of text itself is added to that, so that
code inside a heading is drawn as large as the heading is.

**Arguments**:

- `kind` - What the piece of the note holding the run of text is.
- `styles` - What is said about that run of text.
  

**Returns**:

  The font to draw it with.

<a id="notesmgr.note_fonts.font_tag"></a>

#### font\_tag

```python
def font_tag(key: FontKey) -> str
```

Return the name of the text tag that carries one of the fonts.

<a id="notesmgr.note_fonts.NoteFonts"></a>

## NoteFonts Objects

```python
class NoteFonts()
```

The fonts that a note is drawn with, made larger all together.

A font is made when a note first needs it and is then kept, so
that a note of headings and code brings its fonts along while a
note of plain text needs one. Changing the size configures every
font that was made, and the text tags that carry them draw with
the new size from then on without being touched.

<a id="notesmgr.note_fonts.NoteFonts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(widget: tkinter.Misc, size: Optional[int] = None) -> None
```

Get ready to draw a note with fonts of a size.

**Arguments**:

- `widget` - The widget that the fonts belong to, which is
  what Tk is asked about the system's own fonts over.
- `size` - The size to draw the ordinary text of a note in,
  None for the size that Tk draws text in.

<a id="notesmgr.note_fonts.NoteFonts.font"></a>

#### font

```python
def font(key: FontKey) -> Font
```

Return the font of a key, made the first time it is asked for.

<a id="notesmgr.note_fonts.NoteFonts._make"></a>

#### \_make

```python
def _make(key: FontKey) -> Font
```

Make the font of a key, in the size that is drawn in now.

<a id="notesmgr.note_fonts.NoteFonts.scaled"></a>

#### scaled

```python
def scaled(key: FontKey) -> int
```

Return how large the font of a key is at the size drawn in.

<a id="notesmgr.note_fonts.NoteFonts.resize"></a>

#### resize

```python
def resize(size: int) -> int
```

Draw with fonts of another size from now on.

**Arguments**:

- `size` - The size to draw the ordinary text of a note in.
  

**Returns**:

  The size that is drawn in, which is as near the one
  asked for as a note can be read at.

<a id="notesmgr.note_fonts.NoteFonts.zoom"></a>

#### zoom

```python
def zoom(step: int) -> int
```

Draw so many steps larger, or smaller for a step below zero.

<a id="notesmgr.note_fonts.NoteFonts.normal_size"></a>

#### normal\_size

```python
def normal_size() -> int
```

Draw in the size that the note started out in.

<a id="notesmgr.note_fonts.NoteFonts.indent_step"></a>

#### indent\_step

```python
def indent_step() -> int
```

Return how far one step of indentation is, in pixels.

<a id="notesmgr.note_panel"></a>

# notesmgr.note\_panel

The panel at the right of the main window, showing a note.

<a id="notesmgr.note_panel.PADDING"></a>

#### PADDING

Space in pixels left around what the panel shows.

<a id="notesmgr.note_panel.PLAIN_INSTEAD"></a>

#### PLAIN\_INSTEAD

What is said when the formatting could not be carried along.

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

<a id="notesmgr.note_panel.NotePanel.zoom"></a>

#### zoom

```python
def zoom(step: int) -> None
```

Draw the note so many steps larger, or smaller below zero.

<a id="notesmgr.note_panel.NotePanel.zoom_normal"></a>

#### zoom\_normal

```python
def zoom_normal() -> None
```

Draw the note in the size that it started out in.

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

<a id="notesmgr.note_panel.NotePanel.copied_note"></a>

#### copied\_note

```python
def copied_note() -> Optional[NoteText]
```

Return the note that a copy is taken of, None for none.

A note that could not be read at all holds no text to copy,
so what is wrong with it is reported rather than the
clipboard being emptied. A note that is shown only in part is
copied as far as it is shown, which is what the warning above
it says.

<a id="notesmgr.note_panel.NotePanel.put_on_clipboard"></a>

#### put\_on\_clipboard

```python
def put_on_clipboard(text: str) -> None
```

Put a text on the clipboard, in place of what was on it.

<a id="notesmgr.note_panel.NotePanel.copy_raw"></a>

#### copy\_raw

```python
def copy_raw() -> None
```

Put the text of the note that is shown on the clipboard.

<a id="notesmgr.note_panel.NotePanel.copy_formatted"></a>

#### copy\_formatted

```python
def copy_formatted() -> None
```

Put the note that is shown on the clipboard formatted.

Each platform carries formatted text in a way of its own, and
one that has not got what it needs for it can still carry the
plain text. That is put on the clipboard instead, so that a
copy is never lost, and the user is told why it is plain.

<a id="notesmgr.markdown_render"></a>

# notesmgr.markdown\_render

Turning the markdown of a note into the HTML it is drawn from.

<a id="notesmgr.markdown_render.EXTENSIONS"></a>

#### EXTENSIONS

The markdown that a note may be written in, beyond the plain kind.

Fenced code is how a note holds a program or a command line, tables
are what a note of comparisons is written as, and sane lists keeps a
list from beginning in the middle of a paragraph.

<a id="notesmgr.markdown_render.STRIKE_PATTERN"></a>

#### STRIKE\_PATTERN

What a note marks text that is struck through with.

Two tildes around the text is how it is written everywhere it is
written, and Python-Markdown knows nothing of it, so notesmgr says
what it means rather than taking a dependency for one pattern.

<a id="notesmgr.markdown_render.STRIKE_TAG"></a>

#### STRIKE\_TAG

The HTML that text struck through in a note is turned into.

<a id="notesmgr.markdown_render.STRIKE_NAME"></a>

#### STRIKE\_NAME

What the pattern of text struck through is registered as.

<a id="notesmgr.markdown_render.STRIKE_PRIORITY"></a>

#### STRIKE\_PRIORITY

Where the pattern belongs among the patterns of Python-Markdown.

Just above the emphasis patterns, which is where the marking of a
run of text belongs, and well below the ones for code and links,
so that two tildes inside them are left as the text they are.

<a id="notesmgr.markdown_render.TAB_LENGTH"></a>

#### TAB\_LENGTH

How many spaces one step of indentation is taken to be.

Python-Markdown counts four, which leaves a list nested with two
spaces, as most editors and markdown linters write one, read as a
list of its own rather than as a nested one. Notes are written by
hand, so the smaller step is the one that draws what was meant.

<a id="notesmgr.markdown_render.markdown_converter"></a>

#### markdown\_converter

```python
def markdown_converter() -> markdown.Markdown
```

Return the converter that the HTML of a note is made with.

Python-Markdown passes markup that a note holds straight through
into its output, and a note is read rather than obeyed, so the
two processors that let it through are taken out and the markup
is drawn as the text that it is. Text struck through is added,
which Python-Markdown knows nothing of on its own.

<a id="notesmgr.markdown_render.note_html"></a>

#### note\_html

```python
def note_html(text: str) -> str
```

Return the HTML of a note that is written in markdown.

**Arguments**:

- `text` - The markdown of the note, as much of it as is shown.
  

**Returns**:

  The HTML that the note is drawn from, and that a formatted
  copy of the note is taken from.

<a id="notesmgr.explorer_drag"></a>

# notesmgr.explorer\_drag

Moving the notes and the folders of the tree by dragging them.

<a id="notesmgr.explorer_drag.PRESS_EVENT"></a>

#### PRESS\_EVENT

Tk event of the mouse button going down, which may begin a drag.

<a id="notesmgr.explorer_drag.MOTION_EVENT"></a>

#### MOTION\_EVENT

Tk event of the pointer moving with the mouse button held down.

<a id="notesmgr.explorer_drag.RELEASE_EVENT"></a>

#### RELEASE\_EVENT

Tk event of the mouse button going up, dropping what is dragged.

<a id="notesmgr.explorer_drag.CANCEL_EVENT"></a>

#### CANCEL\_EVENT

Tk event of the key that gives up a drag that is going on.

<a id="notesmgr.explorer_drag.DRAG_START"></a>

#### DRAG\_START

Pixels the pointer moves before a press is taken for a drag.

A press that moves no further than this is the user choosing an item
of the tree rather than taking hold of it, so nothing is marked and
nothing is moved when the button goes up again.

<a id="notesmgr.explorer_drag.MARK_TAG"></a>

#### MARK\_TAG

Name of the tag that marks the folder a drop would land in.

<a id="notesmgr.explorer_drag.MARK_COLOUR"></a>

#### MARK\_COLOUR

Colour of the marks that say where a drop lands, a strong blue.

<a id="notesmgr.explorer_drag.MARK_TEXT_COLOUR"></a>

#### MARK\_TEXT\_COLOUR

Colour of the name of a marked folder, which the mark is behind.

<a id="notesmgr.explorer_drag.LINE_HEIGHT"></a>

#### LINE\_HEIGHT

How thick the line that says where a note lands is, in pixels.

<a id="notesmgr.explorer_drag.Dragging"></a>

## Dragging Objects

```python
class Dragging(NamedTuple)
```

What is being dragged now, and where it would land.

Nothing is being dragged while the item is None, which is how a
drag that was given up and a drag that has not begun are told
from one that is going on.

<a id="notesmgr.explorer_drag.row_at"></a>

#### row\_at

```python
def row_at(tree: ttk.Treeview, height: int) -> Optional[Path]
```

Return the item of a tree at a height, None for no item there.

<a id="notesmgr.explorer_drag.row_box"></a>

#### row\_box

```python
def row_box(tree: ttk.Treeview,
            item: Path) -> Optional[tuple[int, int, int, int]]
```

Return where the row of an item is, None when it is nowhere.

A row that is scrolled out of sight has no place in the tree, and
neither has any row of a window that is not on the screen, which
is what the None is for.

<a id="notesmgr.explorer_drag.lower_half"></a>

#### lower\_half

```python
def lower_half(tree: ttk.Treeview, over: Optional[Path], height: int) -> bool
```

Return whether a height is in the lower half of an item's row.

<a id="notesmgr.explorer_drag.DropMark"></a>

## DropMark Objects

```python
class DropMark()
```

What the tree shows of where a drop would land.

A drop into a folder is shown by marking that folder, and a drop
among the notes of a folder by a line at the edge of a row, which
is where the note would go.

<a id="notesmgr.explorer_drag.DropMark.__init__"></a>

#### \_\_init\_\_

```python
def __init__(tree: ttk.Treeview) -> None
```

Get ready to mark a tree, marking nothing yet.

<a id="notesmgr.explorer_drag.DropMark.at_folder"></a>

#### at\_folder

```python
def at_folder(folder: Path) -> None
```

Mark the folder that what is dragged would be put into.

<a id="notesmgr.explorer_drag.DropMark.at_edge"></a>

#### at\_edge

```python
def at_edge(over: Path, lower: bool) -> None
```

Draw the line at an edge of a row, which a note lands at.

<a id="notesmgr.explorer_drag.DropMark.clear"></a>

#### clear

```python
def clear() -> None
```

Take away the marks that said where a drop would land.

<a id="notesmgr.explorer_drag.ExplorerDrag"></a>

## ExplorerDrag Objects

```python
class ExplorerDrag()
```

Lets what the tree shows be moved by dragging it.

The view supplies nothing but coordinates: which item the pointer
is over, and whether it is in the lower half of that item. Where
that lands the dragged item is answered elsewhere, and this shows
the answer and asks for it to be carried out when the button
goes up.

A drop that lands nowhere is no drop at all, so a release over an
item that nothing can be dropped on, and Escape while dragging,
leave the project exactly as it was.

<a id="notesmgr.explorer_drag.ExplorerDrag.__init__"></a>

#### \_\_init\_\_

```python
def __init__(tree: ttk.Treeview, target: Callable[[Path, Optional[Path], bool],
                                                  Optional[Drop]],
             dropped: Callable[[Path, Drop], None]) -> None
```

Let the items of a tree be dragged from now on.

**Arguments**:

- `tree` - The tree whose items are dragged.
- `target` - Asked where a dragged item would land, given the
  item, what the pointer is over, and whether it is in
  the lower half of that item.
- `dropped` - Told what was dragged and where it was dropped.

<a id="notesmgr.explorer_drag.ExplorerDrag.press"></a>

#### press

```python
def press(event: 'tkinter.Event[ttk.Treeview]') -> None
```

Take hold of the item that the mouse button went down on.

<a id="notesmgr.explorer_drag.ExplorerDrag.motion"></a>

#### motion

```python
def motion(event: 'tkinter.Event[ttk.Treeview]') -> None
```

Show where what is being dragged would land now.

<a id="notesmgr.explorer_drag.ExplorerDrag.release"></a>

#### release

```python
def release(_event: 'tkinter.Event[ttk.Treeview]') -> None
```

Move what was dragged to where it was dropped.

<a id="notesmgr.explorer_drag.ExplorerDrag.cancelled"></a>

#### cancelled

```python
def cancelled(_event: 'tkinter.Event[ttk.Treeview]') -> None
```

Give up the drag, leaving the project exactly as it was.

<a id="notesmgr.explorer_drag.ExplorerDrag.cancel"></a>

#### cancel

```python
def cancel() -> None
```

Forget what was dragged, and unmark where it would land.

<a id="notesmgr.explorer_drag.ExplorerDrag.dragging"></a>

#### dragging

```python
def dragging(height: int) -> bool
```

Return whether the press has become a drag by now.

**Arguments**:

- `height` - Where the pointer is in the tree.
  

**Returns**:

  Whether the pointer has moved far enough from where the
  button went down, which it goes on having done for the
  rest of the drag.

<a id="notesmgr.explorer_drag.ExplorerDrag.show"></a>

#### show

```python
def show(over: Optional[Path], lower: bool) -> None
```

Mark where what is dragged would land, or mark nothing.

**Arguments**:

- `over` - The item of the tree that the pointer is over.
- `lower` - Whether the pointer is in the lower half of it.

<a id="notesmgr.explorer_font"></a>

# notesmgr.explorer\_font

The font that the explorer draws with, and how large it is.

<a id="notesmgr.explorer_font.ROW_PADDING"></a>

#### ROW\_PADDING

Space in pixels that a row of the tree has beyond its text.

<a id="notesmgr.explorer_font.STYLE_KIND"></a>

#### STYLE\_KIND

What a style of a tree must be called for the tree to take it.

<a id="notesmgr.explorer_font.STYLE_NUMBERS"></a>

#### STYLE\_NUMBERS

Numbers that tell the style of one tree from the style of another.

<a id="notesmgr.explorer_font.TreeFont"></a>

## TreeFont Objects

```python
class TreeFont()
```

The font of one tree, and the style that the tree takes it from.

A ttk widget is drawn with the font of its style rather than with
a font of its own, so the tree is given a style of its own here,
and drawing it larger or smaller is that one font being resized.
The rows are made as high as the font needs, so that a name is
not cut off by a row that stayed as high as it was.

The font is the one that Tk draws text with on this system, which
is where a note starts out as well, so that the tree and the note
beside it are read in one size.

<a id="notesmgr.explorer_font.TreeFont.__init__"></a>

#### \_\_init\_\_

```python
def __init__(widget: tkinter.Misc) -> None
```

Make the style of one tree, in the size the system gives.

**Arguments**:

- `widget` - The widget that the font and the style belong to.

<a id="notesmgr.explorer_font.TreeFont.apply"></a>

#### apply

```python
def apply() -> None
```

Let the tree be drawn with the font as it now stands.

<a id="notesmgr.explorer_font.TreeFont.row_height"></a>

#### row\_height

```python
def row_height() -> int
```

Return how high a row is, which the font says.

<a id="notesmgr.explorer_font.TreeFont.resize"></a>

#### resize

```python
def resize(size: int) -> int
```

Draw with a font of another size from now on.

**Arguments**:

- `size` - The size to draw the tree in.
  

**Returns**:

  The size that is drawn in, which is as near the one asked
  for as a tree can be read at.

<a id="notesmgr.explorer_font.TreeFont.zoom"></a>

#### zoom

```python
def zoom(step: int) -> int
```

Draw so many steps larger, or smaller for a step below zero.

<a id="notesmgr.explorer_font.TreeFont.normal_size"></a>

#### normal\_size

```python
def normal_size() -> int
```

Draw in the size that the tree started out in.

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

<a id="notesmgr.note_image"></a>

# notesmgr.note\_image

Which file an image of a note names, and how large it is drawn.

<a id="notesmgr.note_image.MAX_IMAGE_WIDTH"></a>

#### MAX\_IMAGE\_WIDTH

Widest that an image of a note is drawn, in pixels.

An image wider than this is drawn smaller, so that a note holding a
screenshot of a whole screen can still be read in the panel.

<a id="notesmgr.note_image.is_remote"></a>

#### is\_remote

```python
def is_remote(target: str) -> bool
```

Return whether what an image of a note names is on the network.

A scheme of a single letter is the drive of a path on Microsoft
Windows rather than a scheme of a URL, which is the one case
that tells a path from an address.

**Arguments**:

- `target` - What the note names the image as.
  

**Returns**:

  Whether that is an address rather than a file.

<a id="notesmgr.note_image.image_path"></a>

#### image\_path

```python
def image_path(folder: Optional[Path], target: str) -> Optional[Path]
```

Return the file that an image of a note names, None for none.

An image is looked for beside the note rather than in the folder
that the program was started from, because that is where a note
that names an image of its own keeps it. An image that is
somewhere on the network is not fetched at all, so that reading
a note never waits for anything.

**Arguments**:

- `folder` - The folder that holds the note, None when the note
  is shown from nowhere in particular.
- `target` - What the note names the image as.
  

**Returns**:

  The file to draw, None where the note names no file that can
  be drawn from where it stands.

<a id="notesmgr.note_image.shrink_factor"></a>

#### shrink\_factor

```python
def shrink_factor(width: int, limit: int = MAX_IMAGE_WIDTH) -> int
```

Return by how much an image wider than the panel is drawn smaller.

**Arguments**:

- `width` - How wide the image is, in pixels.
- `limit` - How wide it may be drawn, in pixels.
  

**Returns**:

  The smallest whole factor that brings the image within the
  width, which is what Tk can shrink an image by, and one for
  an image that fits as it is.

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
def __init__(parent: tkinter.Misc, on_select: Callable[[Optional[Path]], None],
             on_drop: Callable[[Path, Drop], None]) -> None
```

Build the tree in a frame of its own inside a parent widget.

**Arguments**:

- `parent` - The widget that the explorer is placed in.
- `on_select` - Told which item is selected, whenever that
  changes, and told None when nothing is selected.
- `on_drop` - Told what was dragged in the tree and where it
  was dropped, once the user has let go of it.

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

<a id="notesmgr.explorer_tree.ExplorerTree.drop_at"></a>

#### drop\_at

```python
def drop_at(dragged: Path, over: Optional[Path],
            lower: bool) -> Optional[Drop]
```

Return where a dragged item would land, None for nowhere.

**Arguments**:

- `dragged` - The item that is being dragged.
- `over` - The item of the tree that the pointer is over,
  None when it is over no item at all.
- `lower` - Whether the pointer is in the lower half of it.
  

**Returns**:

  Where the item lands, None when it lands nowhere, which
  is what every drag does while no project is open.

<a id="notesmgr.explorer_tree.ExplorerTree.zoom"></a>

#### zoom

```python
def zoom(step: int) -> None
```

Draw the tree so many steps larger, or smaller below zero.

<a id="notesmgr.explorer_tree.ExplorerTree.zoom_normal"></a>

#### zoom\_normal

```python
def zoom_normal() -> None
```

Draw the tree in the size that it started out in.

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

<a id="notesmgr.clipboard_macos"></a>

# notesmgr.clipboard\_macos

Putting a formatted copy of a note on the pasteboard of macOS.

<a id="notesmgr.clipboard_macos.TEXTUTIL"></a>

#### TEXTUTIL

What turns the HTML of a note into the rich text that macOS pastes.

It is part of macOS itself, so a formatted copy costs notesmgr no
dependency of its own.

<a id="notesmgr.clipboard_macos.SCRIPT"></a>

#### SCRIPT

What puts both shapes of a copy on the pasteboard in one write.

A second write would replace the first, so the rich text and the
plain text are given to the pasteboard together. They are read from
files rather than written into the script itself, because a note is
longer than a command line may be.

The names here are of two words each because AppleScript knows a
great many words of one: a variable called plain, for one, is a
term of the language already, and setting it is refused.

<a id="notesmgr.clipboard_macos.OSASCRIPT"></a>

#### OSASCRIPT

What runs that script, with the two files as its arguments.

<a id="notesmgr.clipboard_macos.RTF_NAME"></a>

#### RTF\_NAME

What the file holding the rich text of a copy is called.

<a id="notesmgr.clipboard_macos.TEXT_NAME"></a>

#### TEXT\_NAME

What the file holding the plain text of a copy is called.

<a id="notesmgr.clipboard_macos.written"></a>

#### written

```python
def written(folder: Path, name: str, data: bytes) -> str
```

Write one shape of a copy into a folder, and name the file.

**Arguments**:

- `folder` - The folder that the file is written into.
- `name` - What the file is to be called.
- `data` - What the file is to hold.
  

**Returns**:

  The file, named as the script that reads it names it.

<a id="notesmgr.clipboard_macos.copy_to_clipboard"></a>

#### copy\_to\_clipboard

```python
def copy_to_clipboard(payload: RichText) -> None
```

Put a formatted copy of a note on the pasteboard of macOS.

**Arguments**:

- `payload` - The copy to put there.
  

**Raises**:

- `NotesmgrError` - macOS did not take the copy.

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

<a id="notesmgr.clipboard_tool"></a>

# notesmgr.clipboard\_tool

What a formatted copy of a note is, and running what takes it.

The clipboard of Tk carries plain text and nothing else, so a copy
that keeps its formatting is handed to a program of the system
instead. Running such a program and saying what it could not do is
the same on every platform, and is therefore done here.

<a id="notesmgr.clipboard_tool.NOT_INSTALLED"></a>

#### NOT\_INSTALLED

What is said when the system has not got the program it needs.

<a id="notesmgr.clipboard_tool.REFUSED"></a>

#### REFUSED

What is said when the program was there but did not do it.

<a id="notesmgr.clipboard_tool.RichText"></a>

## RichText Objects

```python
class RichText(NamedTuple)
```

A copy of a note in the shapes that a clipboard takes it in.

The HTML is what goes inside the body of a document rather than
a whole document, so that each platform can wrap it the way its
own clipboard asks for. The text is the note as it is written,
which is what a plain text field is pasted with.

<a id="notesmgr.clipboard_tool.said_by"></a>

#### said\_by

```python
def said_by(output: Optional[bytes]) -> str
```

Return what a program wrote about itself, as text.

**Arguments**:

- `output` - What the program wrote on its error output, None
  when nothing was read from it.
  

**Returns**:

  What it said, and nothing at all when it said nothing.

<a id="notesmgr.clipboard_tool.run_tool"></a>

#### run\_tool

```python
def run_tool(argv: Sequence[str], data: bytes, capture: bool = True) -> bytes
```

Run a program of the system, and return what it wrote.

**Arguments**:

- `argv` - The program to run and the arguments to give it.
- `data` - What is written to the program on its input.
- `capture` - Whether to read what the program writes. A program
  that goes on running to own the clipboard, as the ones
  of the X11 and the Wayland desktops do, never closes its
  output, and waiting for that output to end would be
  waiting for the program to end.
  

**Returns**:

  What the program wrote, and nothing when it is not read.
  

**Raises**:

- `NotesmgrError` - The program is not installed, could not be
  started, or refused to do it.

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

<a id="notesmgr.commands.Commands.report_notice"></a>

#### report\_notice

```python
def report_notice(message: str) -> None
```

Tell the user of something that was done in another way.

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

<a id="notesmgr.commands.Commands.drop"></a>

#### drop

```python
def drop(item: Path, drop: Drop) -> None
```

Move what was dragged in the tree to where it was dropped.

**Arguments**:

- `item` - The note or the folder that was dragged.
- `drop` - Where it was dropped, as the tree worked it out.

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

<a id="notesmgr.note_file.MARKDOWN_EXTENSIONS"></a>

#### MARKDOWN\_EXTENSIONS

The extensions of the notes that are written in markdown.

A note named .txt is shown as it is written, because a file that
says it is plain text is read as plain text.

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

<a id="notesmgr.note_file.is_markdown"></a>

#### is\_markdown

```python
def is_markdown(name: str) -> bool
```

Return whether a note is written in markdown.

A note that is, is shown formatted for reading, and every other
note is shown as it is written. The extension of the file says
which it is, whatever the project writes its own notes as, so
that a note that was written elsewhere is read as it was meant.

**Arguments**:

- `name` - File name, without any folders before it.
  

**Returns**:

  Whether the name is the name of a markdown note.

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

<a id="notesmgr.note_view.RULE_TEXT"></a>

#### RULE\_TEXT

What a line across the note is drawn with.

The line is drawn long and is not broken where the window ends, so
that it reaches across however wide the window is made.

<a id="notesmgr.note_view.IMAGE_TEXT"></a>

#### IMAGE\_TEXT

How an image of a note is named where it is not drawn.

<a id="notesmgr.note_view.MISSING_ALT"></a>

#### MISSING\_ALT

What an image that the note gives no description of is called.

<a id="notesmgr.note_view.IMAGE_PADDING"></a>

#### IMAGE\_PADDING

Space in pixels left around an image that is drawn in a note.

<a id="notesmgr.note_view.block_spans"></a>

#### block\_spans

```python
def block_spans(block: Block) -> tuple[Span, ...]
```

Return everything that is written for one piece of a note.

The bullet or the number of a list item and the line of a rule
are drawn rather than read, so they are written here and are no
part of what the note holds.

**Arguments**:

- `block` - The piece of the note that is to be written.
  

**Returns**:

  The runs of text to write, in the order they are written in.

<a id="notesmgr.note_view.image_text"></a>

#### image\_text

```python
def image_text(span: Span) -> str
```

Return how an image is named where the image is not drawn.

<a id="notesmgr.note_view.NoteView"></a>

## NoteView Objects

```python
class NoteView()
```

Shows the text of one note, with any warning above it.

The warning is what could not be shown and why, and it is left
out of the way whenever there is nothing to warn about. A note
written in markdown is shown formatted for reading, and every
other note is shown as it is written.

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
def show(note: NoteText,
         formatted: bool = False,
         folder: Optional[Path] = None) -> None
```

Show a note that was read, warning and all.

**Arguments**:

- `note` - The text to show and the warning to show above it.
- `formatted` - Whether the note is written in markdown and
  is therefore shown formatted for reading rather than
  as it is written.
- `folder` - The folder that holds the note, which is where
  an image that the note shows is looked for.

<a id="notesmgr.note_view.NoteView.show_warning"></a>

#### show\_warning

```python
def show_warning(warning: str) -> None
```

Show a warning above the note, and none when there is none.

<a id="notesmgr.note_view.NoteView._writing"></a>

#### \_writing

```python
@contextmanager
def _writing() -> Iterator[None]
```

Empty the area and let it be written to, and no longer.

<a id="notesmgr.note_view.NoteView.show_text"></a>

#### show\_text

```python
def show_text(text: str) -> None
```

Show a text in an area that the user cannot type in.

<a id="notesmgr.note_view.NoteView.show_blocks"></a>

#### show\_blocks

```python
def show_blocks(blocks: Sequence[Block],
                folder: Optional[Path] = None) -> None
```

Show the pieces that a note formatted for reading is drawn in.

**Arguments**:

- `blocks` - The pieces of the note, in the order they are
  drawn in.
- `folder` - The folder that holds the note, which is where
  an image that the note shows is looked for.

<a id="notesmgr.note_view.NoteView._write_gap"></a>

#### \_write\_gap

```python
def _write_gap(block: Block, previous: Optional[Block]) -> None
```

Leave room above a piece of a note that follows another.

<a id="notesmgr.note_view.NoteView._write_block"></a>

#### \_write\_block

```python
def _write_block(block: Block) -> None
```

Write one piece of a note with the tags it is drawn with.

<a id="notesmgr.note_view.NoteView._write_span"></a>

#### \_write\_span

```python
def _write_span(kind: BlockKind, span: Span, indent: str) -> None
```

Write one run of text of a piece of a note.

An image is drawn where its file can be drawn, and is named
by its description where it cannot, so that a note always
says what belongs where the image is.

<a id="notesmgr.note_view.NoteView._write_text"></a>

#### \_write\_text

```python
def _write_text(kind: BlockKind, span: Span, indent: str) -> None
```

Write the text of one run of text, image and all.

<a id="notesmgr.note_view.NoteView._draw_picture"></a>

#### \_draw\_picture

```python
def _draw_picture(picture: tkinter.PhotoImage, indent: str) -> None
```

Draw a picture where the note shows it, indented as it is.

<a id="notesmgr.note_view.NoteView._picture"></a>

#### \_picture

```python
def _picture(span: Span) -> Optional[tkinter.PhotoImage]
```

Return the picture of an image of the note, None for none.

Tk reads PNG and GIF files of its own, and every other file
is named rather than drawn. The pictures of the note are
kept while it is shown, because Tk draws a picture that is
nothing but the tag of an image no longer.

<a id="notesmgr.note_view.NoteView._fitted"></a>

#### \_fitted

```python
def _fitted(picture: tkinter.PhotoImage) -> tkinter.PhotoImage
```

Return a picture drawn small enough to be read in the panel.

<a id="notesmgr.note_view.NoteView.zoom"></a>

#### zoom

```python
def zoom(step: int) -> None
```

Draw the note so many steps larger, or smaller below zero.

<a id="notesmgr.note_view.NoteView.zoom_normal"></a>

#### zoom\_normal

```python
def zoom_normal() -> None
```

Draw the note in the size that it started out in.

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

<a id="notesmgr.project.folder_at"></a>

#### folder\_at

```python
def folder_at(tree: Folder, path: Path) -> Optional[Folder]
```

Return the folder of a tree that is at a path, None for none.

**Arguments**:

- `tree` - The folder to look in, and every folder below it.
- `path` - The folder that is looked for.
  

**Returns**:

  The folder as the tree holds it, None when the tree holds no
  folder of that path, which is what a note or a template of
  the tree leaves behind.

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

<a id="notesmgr.folder_ops.NOT_MOVED"></a>

#### NOT\_MOVED

What is said about a folder that could not be moved.

<a id="notesmgr.folder_ops.INTO_ITSELF"></a>

#### INTO\_ITSELF

What is said about a folder that would be put inside its own tree.

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

<a id="notesmgr.folder_ops.move_folder"></a>

#### move\_folder

```python
def move_folder(folder: Path, parent: Path) -> Path
```

Move a folder of the project into another folder of it.

Everything the folder holds goes along with it, and no note order
is touched: a note order lists the notes of one folder and knows
nothing of the folders beside them.

**Arguments**:

- `folder` - The folder to move.
- `parent` - The folder it is to be in.
  

**Returns**:

  The folder where it now is, which is where it was when it is
  in that folder already.
  

**Raises**:

- `NotesmgrError` - The folder is the root folder of the project,
  it would be put inside its own tree, the name is taken in
  the other folder already, or the folder cannot be moved.


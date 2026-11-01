#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import locale
import gettext
import urllib.parse
from datetime import datetime
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib, Pango, GdkPixbuf

# Translation setup
APPNAME = "pars-mycomputer"
LOCAL_LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "po"))
SYSTEM_LOCALE_DIR = "/usr/share/locale"

try:
    locale.setlocale(locale.LC_ALL, "")
except Exception:
    try:
        locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
    except Exception:
        pass

TRANSLATIONS_PATH = SYSTEM_LOCALE_DIR
if not os.path.isfile(os.path.join(SYSTEM_LOCALE_DIR, "tr", "LC_MESSAGES", f"{APPNAME}.mo")):
    if os.path.isdir(LOCAL_LOCALE_DIR):
        TRANSLATIONS_PATH = LOCAL_LOCALE_DIR

locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
try:
    gettext.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
    gettext.textdomain(APPNAME)
except Exception:
    pass

# Direct translation dictionary for guaranteed Turkish UI
TR_DICT = {
    "Name": "Ad",
    "Size": "Boyut",
    "Type": "Tür",
    "Date Modified": "Değiştirilme Tarihi",
    "Folder": "Klasör",
    "File": "Dosya",
    "Recent": "Son Kullanılan",
    "Recent Files": "Son Kullanılan Dosyalar",
    "Recent files": "Son kullanılan dosyalar",
    "Trash": "Çöp Kutusu",
    "Trash is empty": "Çöp kutusu boş",
    "Back / Upper Directory": "Geri / Üst Dizin",
    "Return to My Computer": "Bilgisayarım'a Dön",
    "Open in external file manager": "Harici dosya yöneticisinde aç",
    "Show Hidden Files": "Gizli Dosyaları Göster",
    "Refresh": "Yenile",
    "items": "öğe",
    "folders": "klasör",
    "files": "dosya",
    "Total": "Toplam",
    "Permission denied": "Erişim engellendi",
    "Could not load recent files": "Son dosyalar yüklenemedi",
    "Could not load trash": "Çöp kutusu yüklenemedi",
}

try:
    _tr_cat = gettext.translation(APPNAME, localedir=TRANSLATIONS_PATH, languages=['tr'], fallback=True)
    def _(msg):
        res = locale.gettext(msg)
        if (res == msg or not res) and _tr_cat:
            res = _tr_cat.gettext(msg)
        if (res == msg or not res) and msg in TR_DICT:
            res = TR_DICT[msg]
        return res
except Exception:
    def _(msg):
        return TR_DICT.get(msg, locale.gettext(msg))


class FileBrowserView(Gtk.Box):
    def __init__(self, on_home_callback=None, on_open_external_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_name("file_browser_container")

        self.on_home_callback = on_home_callback
        self.on_open_external_callback = on_open_external_callback

        self.current_path = ""
        self.history = []
        self.show_hidden = False
        self.icon_cache = {}
        self.icon_theme = Gtk.IconTheme.get_default()

        # Build UI
        self._build_toolbar()
        self._build_content()
        self._build_statusbar()

    def _build_toolbar(self):
        toolbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar_box.set_name("file_browser_toolbar")
        toolbar_box.set_margin_start(12)
        toolbar_box.set_margin_end(12)
        toolbar_box.set_margin_top(8)
        toolbar_box.set_margin_bottom(8)

        # 1. Back button
        self.btn_back = Gtk.Button.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON)
        self.btn_back.set_tooltip_text(_("Back / Upper Directory"))
        self.btn_back.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_back.connect("clicked", self._on_btn_back_clicked)
        toolbar_box.pack_start(self.btn_back, False, False, 0)

        # 2. Home / Overview button
        self.btn_home = Gtk.Button.new_from_icon_name("computer-symbolic", Gtk.IconSize.BUTTON)
        self.btn_home.set_tooltip_text(_("Return to My Computer"))
        self.btn_home.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_home.connect("clicked", self._on_btn_home_clicked)
        toolbar_box.pack_start(self.btn_home, False, False, 0)

        # 3. Path Entry (address bar)
        self.entry_path = Gtk.Entry()
        self.entry_path.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "folder-symbolic")
        self.entry_path.set_hexpand(True)
        self.entry_path.connect("activate", self._on_entry_path_activate)
        toolbar_box.pack_start(self.entry_path, True, True, 0)

        # 4. Refresh button
        self.btn_refresh = Gtk.Button.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON)
        self.btn_refresh.set_tooltip_text(_("Refresh"))
        self.btn_refresh.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_refresh.connect("clicked", lambda b: self.refresh())
        toolbar_box.pack_start(self.btn_refresh, False, False, 0)

        # 5. Show hidden files toggle button
        self.btn_hidden = Gtk.ToggleButton()
        img_hidden = Gtk.Image.new_from_icon_name("view-more-symbolic", Gtk.IconSize.BUTTON)
        self.btn_hidden.set_image(img_hidden)
        self.btn_hidden.set_tooltip_text(_("Show Hidden Files"))
        self.btn_hidden.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_hidden.connect("toggled", self._on_btn_hidden_toggled)
        toolbar_box.pack_start(self.btn_hidden, False, False, 0)

        # 6. Open in external file manager button
        self.btn_external = Gtk.Button.new_from_icon_name("folder-remote-symbolic", Gtk.IconSize.BUTTON)
        self.btn_external.set_tooltip_text(_("Open in external file manager"))
        self.btn_external.set_relief(Gtk.ReliefStyle.NONE)
        self.btn_external.connect("clicked", self._on_btn_external_clicked)
        toolbar_box.pack_start(self.btn_external, False, False, 0)

        self.pack_start(toolbar_box, False, False, 0)

    def _build_content(self):
        # InfoBar for messages / errors
        self.infobar = Gtk.InfoBar()
        self.infobar.set_revealed(False)
        self.infobar.set_show_close_button(True)
        self.infobar.connect("response", lambda ib, resp: ib.set_revealed(False))
        self.infobar_label = Gtk.Label(label="")
        self.infobar.get_content_area().pack_start(self.infobar_label, True, True, 0)
        self.pack_start(self.infobar, False, False, 0)

        # ScrolledWindow with TreeView
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_vexpand(True)
        self.scrolled_window.set_hexpand(True)

        # ListStore:
        # 0: icon (Pixbuf)
        # 1: name (str)
        # 2: size_str (str)
        # 3: type_str (str)
        # 4: mtime_str (str)
        # 5: is_dir (bool)
        # 6: full_path (str)
        # 7: sort_name (str)
        # 8: raw_size (int)
        # 9: raw_mtime (float)
        self.liststore = Gtk.ListStore(
            GdkPixbuf.Pixbuf,
            str,
            str,
            str,
            str,
            bool,
            str,
            str,
            int,
            float
        )

        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.set_name("file_browser_treeview")
        self.treeview.set_headers_visible(True)
        self.treeview.connect("row-activated", self._on_row_activated)
        self.treeview.connect("key-press-event", self._on_key_press_event)

        # Column 1: Name (Icon + Text)
        col_name = Gtk.TreeViewColumn(_("Name"))
        col_name.set_resizable(True)
        col_name.set_expand(True)
        col_name.set_min_width(220)
        col_name.set_sort_column_id(7)

        cell_icon = Gtk.CellRendererPixbuf()
        cell_icon.set_property("xpad", 6)
        col_name.pack_start(cell_icon, False)
        col_name.add_attribute(cell_icon, "pixbuf", 0)

        cell_name = Gtk.CellRendererText()
        cell_name.set_property("ellipsize", Pango.EllipsizeMode.END)
        col_name.pack_start(cell_name, True)
        col_name.add_attribute(cell_name, "text", 1)
        self.treeview.append_column(col_name)

        # Column 2: Size
        col_size = Gtk.TreeViewColumn(_("Size"))
        col_size.set_resizable(True)
        col_size.set_min_width(100)
        col_size.set_sort_column_id(8)
        cell_size = Gtk.CellRendererText()
        cell_size.set_property("xalign", 1.0)
        col_size.pack_start(cell_size, True)
        col_size.add_attribute(cell_size, "text", 2)
        self.treeview.append_column(col_size)

        # Column 3: Type
        col_type = Gtk.TreeViewColumn(_("Type"))
        col_type.set_resizable(True)
        col_type.set_min_width(120)
        col_type.set_sort_column_id(3)
        cell_type = Gtk.CellRendererText()
        col_type.pack_start(cell_type, True)
        col_type.add_attribute(cell_type, "text", 3)
        self.treeview.append_column(col_type)

        # Column 4: Modified
        col_mtime = Gtk.TreeViewColumn(_("Date Modified"))
        col_mtime.set_resizable(True)
        col_mtime.set_min_width(140)
        col_mtime.set_sort_column_id(9)
        cell_mtime = Gtk.CellRendererText()
        col_mtime.pack_start(cell_mtime, True)
        col_mtime.add_attribute(cell_mtime, "text", 4)
        self.treeview.append_column(col_mtime)

        # Set default sort: by sort_name (dirs first, then alphabetical)
        self.liststore.set_sort_column_id(7, Gtk.SortType.ASCENDING)

        self.scrolled_window.add(self.treeview)
        self.pack_start(self.scrolled_window, True, True, 0)

    def _build_statusbar(self):
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        status_box.set_name("file_browser_statusbar")
        status_box.set_margin_start(12)
        status_box.set_margin_end(12)
        status_box.set_margin_top(4)
        status_box.set_margin_bottom(4)

        self.lbl_status = Gtk.Label(label="")
        self.lbl_status.set_halign(Gtk.Align.START)
        status_box.pack_start(self.lbl_status, False, False, 0)

        self.pack_start(status_box, False, False, 0)

    def load_directory(self, target_path, add_to_history=True):
        """Loads and displays the contents of target_path (supports local paths, recent:///, trash:///)."""
        if not target_path:
            return

        target_str = str(target_path).strip()

        # Handle Recent Files inside internal browser
        if target_str in ("recent:///", "recent://") or target_str.startswith("recent:///"):
            self._load_recent(add_to_history)
            return

        # Handle Trash inside internal browser
        if target_str in ("trash:///", "trash://") or target_str.startswith("trash:///"):
            self._load_trash(add_to_history)
            return

        # Remote network protocols that require external file manager
        if target_str.startswith(("computer://", "smb://", "sftp://", "ftp://", "dav://", "davs://", "mtp://", "gphoto2://")):
            if self.on_open_external_callback:
                self.on_open_external_callback(target_str)
            return

        if target_str.startswith("file://"):
            target_str = urllib.parse.unquote(target_str[7:])

        target_path = os.path.abspath(os.path.expanduser(target_str))

        if not os.path.exists(target_path):
            self._show_error(_(f"Path does not exist: {target_path}"))
            return

        if not os.path.isdir(target_path):
            # It's a file, open it directly
            self._open_file(target_path)
            return

        if add_to_history and self.current_path and self.current_path != target_path:
            self.history.append(self.current_path)

        self.current_path = target_path
        self.entry_path.set_text(self.current_path)
        self.infobar.set_revealed(False)
        self.liststore.clear()

        dir_count = 0
        file_count = 0
        total_size = 0

        try:
            with os.scandir(target_path) as entries:
                for entry in entries:
                    name = entry.name
                    if not self.show_hidden and name.startswith("."):
                        continue

                    try:
                        stat = entry.stat(follow_symlinks=False)
                        is_dir = entry.is_dir(follow_symlinks=True)
                        raw_size = stat.st_size if not is_dir else 0
                        raw_mtime = stat.st_mtime
                        mtime_str = datetime.fromtimestamp(raw_mtime).strftime("%Y-%m-%d %H:%M")
                    except (PermissionError, FileNotFoundError, OSError):
                        is_dir = False
                        raw_size = 0
                        raw_mtime = 0
                        mtime_str = "-"

                    if is_dir:
                        dir_count += 1
                        icon = self._get_folder_icon(name)
                        size_str = _("Folder")
                        type_str = _("Folder")
                        sort_name = f"0_{name.lower()}"
                    else:
                        file_count += 1
                        total_size += raw_size
                        icon = self._get_file_icon(name, entry.path)
                        size_str = self._format_size(raw_size)
                        type_str = self._get_file_type_description(name, entry.path)
                        sort_name = f"1_{name.lower()}"

                    self.liststore.append([
                        icon,
                        name,
                        size_str,
                        type_str,
                        mtime_str,
                        is_dir,
                        entry.path,
                        sort_name,
                        raw_size,
                        raw_mtime
                    ])

            total_size_str = self._format_size(total_size)
            self.lbl_status.set_text(
                f"{dir_count} " + _("folders") + f", {file_count} " + _("files") + f" — " + _("Total") + f": {total_size_str}"
            )

        except PermissionError:
            self._show_error(_(f"Permission denied: {target_path}"))
            self.lbl_status.set_text(_("Permission denied"))
        except Exception as e:
            self._show_error(f"{e}")
            self.lbl_status.set_text(f"{e}")

    def _load_recent(self, add_to_history=True):
        """Loads recently used files from Gtk.RecentManager inside the internal browser."""
        if add_to_history and self.current_path and self.current_path != "recent:///":
            self.history.append(self.current_path)

        self.current_path = "recent:///"
        self.entry_path.set_text("recent:///")
        self.infobar.set_revealed(False)
        self.liststore.clear()

        dir_count = 0
        file_count = 0
        total_size = 0

        try:
            rm = Gtk.RecentManager.get_default()
            items = [item for item in rm.get_items() if item.exists()]
            items.sort(key=lambda x: x.get_visited() or x.get_modified() or 0, reverse=True)

            for item in items:
                name = item.get_display_name() or os.path.basename(item.get_uri_display() or "")
                uri = item.get_uri()
                local_path = None
                if uri.startswith("file://"):
                    local_path = urllib.parse.unquote(uri[7:])

                is_dir = (item.get_mime_type() == "inode/directory" or (local_path and os.path.isdir(local_path)))
                raw_size = 0
                if local_path and os.path.isfile(local_path):
                    try:
                        raw_size = os.path.getsize(local_path)
                    except Exception:
                        raw_size = 0

                ts = item.get_visited() or item.get_modified() or 0
                mtime_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M") if ts else "-"

                if is_dir:
                    dir_count += 1
                    icon = self._get_folder_icon(name)
                    size_str = _("Folder")
                    type_str = _("Folder")
                    sort_name = f"0_{name.lower()}"
                else:
                    file_count += 1
                    total_size += raw_size
                    icon = self._get_file_icon(name, local_path or name)
                    size_str = self._format_size(raw_size)
                    type_str = self._get_file_type_description(name, local_path or name)
                    sort_name = f"1_{name.lower()}"

                target_row_path = local_path if local_path else uri
                self.liststore.append([
                    icon,
                    name,
                    size_str,
                    type_str,
                    mtime_str,
                    is_dir,
                    target_row_path,
                    sort_name,
                    raw_size,
                    float(ts)
                ])

            total_str = self._format_size(total_size)
            self.lbl_status.set_text(
                f"{len(items)} " + _("items") + f" ({_('Recent')}) — " + _("Total") + f": {total_str}"
            )
        except Exception as e:
            self._show_error(f"{_('Could not load recent files')}: {e}")

    def _load_trash(self, add_to_history=True):
        """Loads trash:/// contents inside the internal browser."""
        if add_to_history and self.current_path and self.current_path != "trash:///":
            self.history.append(self.current_path)

        self.current_path = "trash:///"
        self.entry_path.set_text("trash:///")
        self.infobar.set_revealed(False)
        self.liststore.clear()

        dir_count = 0
        file_count = 0
        total_size = 0

        try:
            trash_gfile = Gio.File.new_for_uri("trash:///")
            enumerator = trash_gfile.enumerate_children(
                "standard::*,trash::*", Gio.FileQueryInfoFlags.NONE, None
            )

            for info in enumerator:
                name = info.get_display_name() or info.get_name()
                is_dir = (info.get_file_type() == Gio.FileType.DIRECTORY)
                raw_size = info.get_size() or 0

                del_date_str = info.get_attribute_as_string("trash::deletion-date")
                mtime_str = "-"
                ts = 0.0
                if del_date_str:
                    try:
                        clean_date = del_date_str.replace("T", " ")[:16]
                        mtime_str = clean_date
                    except Exception:
                        mtime_str = del_date_str

                if is_dir:
                    dir_count += 1
                    icon = self._get_folder_icon(name)
                    size_str = _("Folder")
                    type_str = _("Folder")
                    sort_name = f"0_{name.lower()}"
                else:
                    file_count += 1
                    total_size += raw_size
                    icon = self._get_file_icon(name, name)
                    size_str = self._format_size(raw_size)
                    type_str = self._get_file_type_description(name, name)
                    sort_name = f"1_{name.lower()}"

                # Actual local path in ~/.local/share/Trash/files if available
                trash_local_dir = os.path.expanduser("~/.local/share/Trash/files")
                local_candidate = os.path.join(trash_local_dir, info.get_name())
                if os.path.exists(local_candidate):
                    target_row_path = local_candidate
                else:
                    child_gfile = trash_gfile.get_child(info.get_name())
                    target_row_path = child_gfile.get_uri()

                self.liststore.append([
                    icon,
                    name,
                    size_str,
                    type_str,
                    mtime_str,
                    is_dir,
                    target_row_path,
                    sort_name,
                    raw_size,
                    ts
                ])

            total_str = self._format_size(total_size)
            if (dir_count + file_count) == 0:
                self.lbl_status.set_text(_("Trash is empty"))
            else:
                self.lbl_status.set_text(
                    f"{dir_count + file_count} " + _("items") + f" ({_('Trash')}) — " + _("Total") + f": {total_str}"
                )
        except Exception as e:
            self._show_error(f"{_('Could not load trash')}: {e}")

    def refresh(self):
        if self.current_path:
            self.load_directory(self.current_path, add_to_history=False)

    def _show_error(self, message):
        self.infobar_label.set_text(message)
        self.infobar.set_message_type(Gtk.MessageType.WARNING)
        self.infobar.set_revealed(True)

    def _on_btn_back_clicked(self, button):
        # 1. Try history
        if self.history:
            prev = self.history.pop()
            if prev in ("trash:///", "recent:///") or os.path.exists(prev):
                self.load_directory(prev, add_to_history=False)
                return

        # 2. If in trash or recent without history, return to home
        if self.current_path in ("trash:///", "recent:///"):
            self._on_btn_home_clicked(None)
            return

        # 3. If no history, try parent directory
        if self.current_path:
            parent = os.path.dirname(self.current_path.rstrip("/"))
            if parent and parent != self.current_path and os.path.exists(parent):
                self.load_directory(parent, add_to_history=False)
                return

        # 4. Otherwise return to home overview
        self._on_btn_home_clicked(None)

    def _on_btn_home_clicked(self, button):
        if self.on_home_callback:
            self.on_home_callback()

    def _on_btn_external_clicked(self, button):
        if self.on_open_external_callback and self.current_path:
            self.on_open_external_callback(self.current_path)

    def _on_btn_hidden_toggled(self, button):
        self.show_hidden = button.get_active()
        self.refresh()

    def _on_entry_path_activate(self, entry):
        path = entry.get_text().strip()
        if path:
            self.load_directory(path)

    def _on_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        iter_ = model.get_iter(path)
        is_dir = model.get_value(iter_, 5)
        full_path = model.get_value(iter_, 6)

        if is_dir:
            self.load_directory(full_path)
        else:
            self._open_file(full_path)

    def _on_key_press_event(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_BackSpace:
            self._on_btn_back_clicked(None)
            return True
        elif keyval == Gdk.KEY_Left and (event.state & Gdk.ModifierType.MOD1_MASK):
            self._on_btn_back_clicked(None)
            return True
        return False

    def _open_file(self, file_path):
        """Opens a file with default application."""
        if str(file_path).startswith("trash://"):
            try:
                Gio.AppInfo.launch_default_for_uri(file_path, None)
                return
            except Exception:
                pass

        if "://" in str(file_path):
            gio_file = Gio.File.new_for_uri(file_path)
        else:
            gio_file = Gio.File.new_for_path(file_path)

        try:
            display = self.get_display()
            context = display.get_app_launch_context() if display else None
            app_info = gio_file.query_default_handler(None)
            if app_info:
                app_info.launch([gio_file], context)
                return
        except Exception:
            pass

        try:
            subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            self._show_error(_(f"Could not open file: {e}"))

    def _get_folder_icon(self, name):
        name_lower = name.lower()
        icon_name = "folder"
        special_folders = {
            "desktop": "user-desktop",
            "masaüstü": "user-desktop",
            "documents": "folder-documents",
            "belgeler": "folder-documents",
            "downloads": "folder-download",
            "indirilenler": "folder-download",
            "music": "folder-music",
            "müzik": "folder-music",
            "pictures": "folder-pictures",
            "resimler": "folder-pictures",
            "videos": "folder-videos",
            "videolar": "folder-videos",
            "templates": "folder-templates",
            "şablonlar": "folder-templates",
            "public": "folder-publicshare",
            "genel": "folder-publicshare",
            "recent": "document-open-recent-symbolic",
            "trash": "user-trash-symbolic",
            "çöp": "user-trash-symbolic",
        }

        if name_lower in special_folders:
            icon_name = special_folders[name_lower]

        return self._lookup_icon(icon_name, fallback="folder")

    def _get_file_icon(self, name, full_path):
        ext = os.path.splitext(name)[1].lower()
        icon_name = "text-x-generic"

        ext_map = {
            ".png": "image-x-generic",
            ".jpg": "image-x-generic",
            ".jpeg": "image-x-generic",
            ".gif": "image-x-generic",
            ".svg": "image-x-generic",
            ".webp": "image-x-generic",
            ".mp3": "audio-x-generic",
            ".wav": "audio-x-generic",
            ".flac": "audio-x-generic",
            ".ogg": "audio-x-generic",
            ".mp4": "video-x-generic",
            ".mkv": "video-x-generic",
            ".avi": "video-x-generic",
            ".mov": "video-x-generic",
            ".pdf": "application-pdf",
            ".zip": "package-x-generic",
            ".tar": "package-x-generic",
            ".gz": "package-x-generic",
            ".xz": "package-x-generic",
            ".deb": "package-x-generic",
            ".sh": "text-x-script",
            ".py": "text-x-script",
            ".txt": "text-x-generic",
            ".md": "text-x-generic",
            ".json": "text-x-generic",
            ".html": "text-html",
            ".iso": "media-optical",
        }

        if ext in ext_map:
            icon_name = ext_map[ext]
        else:
            try:
                content_type, _ = Gio.content_type_guess(name, None)
                if content_type:
                    icon_obj = Gio.content_type_get_icon(content_type)
                    if icon_obj and hasattr(icon_obj, "get_names"):
                        names = icon_obj.get_names()
                        if names:
                            icon_name = names[0]
            except Exception:
                pass

        return self._lookup_icon(icon_name, fallback="text-x-generic")

    def _lookup_icon(self, icon_name, size=24, fallback="text-x-generic"):
        cache_key = f"{icon_name}_{size}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]

        pixbuf = None
        for name in [icon_name, fallback, "folder", "text-x-generic"]:
            try:
                pixbuf = self.icon_theme.load_icon(name, size, Gtk.IconLookupFlags.GENERIC_FALLBACK)
                if pixbuf:
                    break
            except Exception:
                continue

        if not pixbuf:
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon("text-x-generic", size, 0)
            except Exception:
                pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, size, size)
                pixbuf.fill(0)

        self.icon_cache[cache_key] = pixbuf
        return pixbuf

    def _format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def _get_file_type_description(self, name, full_path):
        ext = os.path.splitext(name)[1].lower().lstrip(".")
        if ext:
            return f"{ext.upper()} " + _("File")
        return _("File")

# Table of Contents

* [notesmgr.main\_window](#notesmgr.main_window)
  * [Shortcut](#notesmgr.main_window.Shortcut)
  * [tk\_window\_system](#notesmgr.main_window.tk_window_system)
  * [quit\_shortcut](#notesmgr.main_window.quit_shortcut)
  * [MainWindow](#notesmgr.main_window.MainWindow)
    * [\_\_init\_\_](#notesmgr.main_window.MainWindow.__init__)
    * [show\_project](#notesmgr.main_window.MainWindow.show_project)
    * [quit](#notesmgr.main_window.MainWindow.quit)
* [notesmgr.application](#notesmgr.application)
  * [main](#notesmgr.application.main)

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

<a id="notesmgr.main_window.MainWindow.show_project"></a>

#### show\_project

```python
def show_project(project_name: Optional[str]) -> None
```

Name the open project in the window title, None meaning none.

<a id="notesmgr.main_window.MainWindow.quit"></a>

#### quit

```python
def quit() -> None
```

Destroy the main window, which ends the application.

<a id="notesmgr.application"></a>

# notesmgr.application

Start-up of the notesmgr application.

<a id="notesmgr.application.main"></a>

#### main

```python
def main() -> None
```

Run the notesmgr graphical user interface until the user quits.


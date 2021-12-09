from pathlib import Path
import stat


def is_under(path: Path, parent: Path) -> bool:
    try:
        _ = path.relative_to(parent)
        return True
    except ValueError:
        return False


class Walker:
    def __init__(self, root: Path) -> None:
        self._walk(root.resolve())

    FILE_PERMS = {
        "user": {
            "r": stat.S_IRUSR,
            "w": stat.S_IWUSR,
            "x": stat.S_IXUSR,
            "s": stat.S_ISUID,
        },
        "group": {
            "r": stat.S_IRGRP,
            "w": stat.S_IWGRP,
            "x": stat.S_IXGRP,
            "s": stat.S_ISGID,
        },
        "others": {"r": stat.S_IROTH, "w": stat.S_IWOTH, "x": stat.S_IXOTH},
    }

    def _walk(self, directory: Path) -> None:
        for path in directory.iterdir():
            if not path.is_symlink():
                if path.is_dir():
                    self.act_on_directory(path)
                    self._walk(path)

                elif path.is_file():
                    self.act_on_file(path)

    def act_on_file(self, path: Path) -> None:

        file_perms = path.stat().st_mode
        group_readable = bool(file_perms & self.FILE_PERMS["group"]["r"])
        group_writeable = bool(file_perms & self.FILE_PERMS["group"]["w"])
        user_readable = bool(file_perms & self.FILE_PERMS["user"]["r"])
        user_writeable = bool(file_perms & self.FILE_PERMS["user"]["w"])
        user_executable = bool(file_perms & self.FILE_PERMS["user"]["x"])
        group_executable = bool(file_perms & self.FILE_PERMS["group"]["x"])

        # check if file has ug+rw and g=u
        # print message if permissions not ok:
        if not group_readable:
            print("file check:" + path.as_posix() + " not group readable")
        if not group_writeable:
            print("file check:" + path.as_posix() + " not group writeable")
        if not user_readable:
            print("file check:" + path.as_posix() + " not user readable")
        if not user_writeable:
            print("file check:" + path.as_posix() + " not user writeable")
        if user_executable and not group_executable:
            print("file check:" + path.as_posix() + " u has x perm but not g")
        if group_executable and not user_executable:
            print("file check:" + path.as_posix() + " g has x perm but not u")

    def act_on_directory(self, directory: Path) -> None:

        dir_perms = directory.stat().st_mode
        group_writeable = bool(dir_perms & self.FILE_PERMS["group"]["w"])
        user_writeable = bool(dir_perms & self.FILE_PERMS["user"]["w"])
        user_executable = bool(dir_perms & self.FILE_PERMS["user"]["x"])
        group_executable = bool(dir_perms & self.FILE_PERMS["group"]["x"])

        # check that directory has ug+wx
        if not group_writeable:
            print("dir check:" + directory.as_posix() + " not group writeable")
        if not user_writeable:
            print("dir check:" + directory.as_posix() + " not user writeable")
        if not group_executable:
            print("dir check:" + directory.as_posix() + " not group executable")
        if not user_executable:
            print("dir check:" + directory.as_posix() + " not user executable")

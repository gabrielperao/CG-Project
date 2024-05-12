import os


class PathHelper:

    @staticmethod
    def __get_project_abs_path():
        cur_dir: str = os.path.abspath(os.getcwd())  # project -> src -> util -> path
        while not os.path.isfile(os.path.join(cur_dir, "readme.md")):
            cur_dir = os.path.dirname(cur_dir)
        return cur_dir

    @classmethod
    def get_abs_path(cls, path: str) -> str:
        project_abs_path: str = cls.__get_project_abs_path()
        return os.path.join(project_abs_path, path)

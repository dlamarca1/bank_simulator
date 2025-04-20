import json
import os


class PersistBankDataJson(dict):
    def __init__(
        self,
        dir_path: str
    ) -> None:
        self.dir_path: str = dir_path
        os.makedirs(
            self.dir_path,
            exist_ok=True
        )

        for filename in os.listdir(
            self.dir_path
        ):
            if filename.endswith(
                '.json'
            ):
                holder_name: str = filename[:-5]
                file_path = os.path.join(
                    self.dir_path,
                    filename
                )
                try:
                    with open(
                        file_path,
                        'r'
                    ) as f:
                        data = json.load(f)
                        super().__setitem__(
                            holder_name,
                            data
                        )
                except (
                    json.JSONDecodeError,
                    IOError
                ):
                    pass

    def _file_path(
        self,
        holder_name: str
    ) -> str:
        return os.path.join(
            self.dir_path,
            f"{holder_name}.json"
        )

    def _save_holder(
        self,
        holder_name: str
    ) -> None:
        file_path = self._file_path(
            holder_name
        )
        with open(
            file_path,
            'w'
        ) as f:
            json.dump(
                self[holder_name],
                f,
                indent=4,
                default=str
            )

    def __setitem__(
        self,
        key,
        value
    ) -> None:
        super().__setitem__(
            key,
            value
        )
        self._save_holder(
            key
        )

    def __delitem__(
        self,
        key
    ) -> None:
        super().__delitem__(
            key
        )
        file_path = self._file_path(
            key
        )
        if os.path.exists(
            file_path
        ):
            os.remove(
                file_path
            )

    def update(
        self,
        *args,
        **kwargs
    ) -> None:
        super().update(
            *args,
            **kwargs
        )
        for holder_name in self.keys():
            self._save_holder(
                holder_name
            )

    def clear(
        self
    ) -> None:
        for holder_name in list(
            self.keys()
        ):
            del self[holder_name]

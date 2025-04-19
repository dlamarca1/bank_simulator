import json
import os


class PersistBankDataJson(dict):
    def __init__(
        self,
        file_path: str
    ) -> None:
        self.file_path: str = file_path

        if os.path.exists(
            file_path
        ):
            with open(
                file_path,
                'r'
            ) as file:
                try:
                    data = json.load(
                        file
                    )
                    super().__init__(
                        data
                    )
                except json.JSONDecodeError:
                    super().__init__()
        else:
            super().__init__()
            self._save()

    def _save(
        self
    ) -> None:
        def convert(
            o
        ) -> str:
            return str(o)

        with open(
            self.file_path,
            'w'
        ) as file:
            json.dump(
                self,
                file,
                indent=4,
                default=convert
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
        self._save()

    def __delitem__(
        self,
        key
    ) -> None:
        super().__delitem__(
            key
        )
        self._save()

    def update(
        self,
        *args,
        **kwargs
    ) -> None:
        super().update(
            *args,
            **kwargs
        )
        self._save()

    def clear(
        self
    ) -> None:
        super().clear()
        self._save()

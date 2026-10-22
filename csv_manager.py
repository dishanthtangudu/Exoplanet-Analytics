import os
import tempfile
import pandas as pd

class CSVManager:
    def __init__(self, file_path, required_columns):
        self.file_path = file_path
        self.required_columns = required_columns
    def read_data(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(
                    f"CSV file not found: {self.file_path}"
                )
            df = pd.read_csv(self.file_path)
            if df.empty:
                raise ValueError("The CSV file is empty.")
            missing_columns = [
                col for col in self.required_columns
                if col not in df.columns
            ]
            if missing_columns:
                raise ValueError(
                    f"Missing columns: {', '.join(missing_columns)}"
                )
        except (FileNotFoundError, pd.errors.EmptyDataError, ValueError) as e:
            raise e
        else:
            return df
        finally:
            pass
    def write_data(self, df):
        temp_path = None
        try:
            folder = os.path.dirname(self.file_path)
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".csv",
                dir=folder,
                delete=False,
                encoding="utf-8",
                newline=""
            ) as temp_file:
                temp_path = temp_file.name
                df.to_csv(temp_path, index=False)
            os.replace(temp_path, self.file_path)
        except (OSError, ValueError) as e:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
        else:
            return True
        finally:
            pass
    def check_duplicate(self, df, column, value):
        return df[column].astype(str).str.lower().eq(
            str(value).lower()
        ).any()
    def create_record(self, record):
        df = self.read_data()
        id_column = self.required_columns[0]
        if self.check_duplicate(df, id_column, record[id_column]):
            raise ValueError(
                f"{id_column} already exists."
            )
        new_row = pd.DataFrame([record])
        df = pd.concat([df, new_row], ignore_index=True)
        self.write_data(df)
        return df
    def update_record(self, record_id, updated_record):
        df = self.read_data()
        id_column = self.required_columns[0]
        matches = df[id_column].astype(str) == str(record_id)
        if not matches.any():
            raise ValueError("Record ID not found.")
        for column, value in updated_record.items():
            if column != id_column:
                df.loc[matches, column] = value
        self.write_data(df)
        return df
    def delete_record(self, record_id):
        df = self.read_data()
        id_column = self.required_columns[0]
        matches = df[id_column].astype(str) == str(record_id)
        if not matches.any():
            raise ValueError("Record ID not found.")
        df = df.loc[~matches].reset_index(drop=True)
        self.write_data(df)
        return df
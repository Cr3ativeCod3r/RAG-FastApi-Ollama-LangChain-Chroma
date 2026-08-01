import os
import pandas as pd
from langchain_core.documents import Document
from app.domain.ports import IDocumentLoader


class ExcelDocumentLoader(IDocumentLoader):
    """Concrete implementation of IDocumentLoader for Excel (.xlsx, .xls) files."""

    def load(self, file_path: str) -> list[Document]:
        """Load and convert Excel rows into structured LangChain Document objects."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at: {file_path}")

        excel_data = pd.read_excel(file_path, sheet_name=None)
        documents: list[Document] = []

        for sheet_name, df in excel_data.items():
            # Clean up empty rows
            df = df.dropna(how="all")
            if df.empty:
                continue

            columns = [str(col).strip() for col in df.columns]

            for index, row in df.iterrows():
                # Build formatted content representation
                row_parts = []
                metadata = {
                    "source": os.path.basename(file_path),
                    "sheet_name": sheet_name,
                    "row_index": int(index) + 2,  # 1-based + 1 for header row
                }

                # Extract key fields if available, otherwise serialize all columns
                for col in df.columns:
                    val = row[col]
                    if pd.notna(val):
                        str_val = str(val).strip()
                        row_parts.append(f"{col}: {str_val}")
                        # Keep short scalar values in metadata for filtering
                        if len(str_val) < 100:
                            metadata[str(col).lower().replace(" ", "_")] = str_val

                if not row_parts:
                    continue

                page_content = "\n".join(row_parts)
                documents.append(Document(page_content=page_content, metadata=metadata))

        return documents

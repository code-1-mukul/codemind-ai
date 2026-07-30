from pathlib import Path
import json

from app.core.config import settings
from app.schemas.embedding import EmbeddedChunk
from app.schemas.metadata import MetadataEntry, MetadataFile


class MetadataService:

    def __init__(self):

        Path(settings.METADATA_STORAGE_DIR).mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_metadata(
    self,
    repository_name: str,
    embedded_chunks: list[EmbeddedChunk],
    ) -> None:
            """
            Save metadata for all indexed chunks.
            """

            entries = []

            for idx, embedded_chunk in enumerate(embedded_chunks):

                entries.append(
                    MetadataEntry(
                        id=idx,
                        chunk=embedded_chunk.chunk,
                    )
                )

            metadata = MetadataFile(entries=entries)

            metadata_path = (
                Path(settings.METADATA_STORAGE_DIR)
                / f"{repository_name}.json"
            )

            with open(metadata_path, "w", encoding="utf-8") as f:

                json.dump(
                    metadata.model_dump(),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

    def load_metadata(
        self,
        repository_name: str,
    ) -> MetadataFile:
        # Load metadata for a repository.

        metadata_path = (
            Path(settings.METADATA_STORAGE_DIR)
                / f"{repository_name}.json"
            )

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return MetadataFile.model_validate(metadata)

    def get_chunk_by_id(
    self,
    repository_name: str,
    chunk_id: int,
    ):
        # Retrieve a chunk by its metadata ID.

        metadata = self.load_metadata(repository_name)

        for entry in metadata.entries:
            if entry.id == chunk_id:
                return entry

        return None

    def get_chunks_by_ids(
    self,
    repository_name: str,
    chunk_ids: list[int],
    ):
    # Retrieve multiple chunks by their IDs.

        metadata = self.load_metadata(repository_name)

        chunk_map = {
            entry.id: entry
            for entry in metadata.entries
        }

        return [
            chunk_map[idx]
            for idx in chunk_ids
            if idx in chunk_map
        ]
    
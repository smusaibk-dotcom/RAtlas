from docling_core.types.doc.document import DoclingDocument


class DocumentChunker:
    def __init__(self):
        self._document = None

        self._current_heading = ""

        self._chunks = []

        self._current_text = []

        self._seen = set()

    def chunk(
        self,
        document: DoclingDocument,
    ):
        self._document = document

        self._chunks = []

        self._current_heading = ""

        self._current_text = []

        self._seen = set()

        self._walk(
            document.body,
        )

        self._flush()

        return self._chunks

    def _walk(self, node):
        if node is None:
            return

        node_type = type(node).__name__

        if node_type in ("GroupItem", "InlineGroup"):
            for ref in node.children:
                self._walk(self._resolve_ref(ref))

            return

        if node_type in ("TitleItem", "SectionHeaderItem"):
            self._flush()

            self._current_heading = node.text

            if hasattr(node, "children"):
                for ref in node.children:
                    self._walk(self._resolve_ref(ref))

            return

        if node_type == "TextItem":
            text = node.text.strip()

            if text:
                self._current_text.append(text)

            if hasattr(node, "children"):
                for ref in node.children:
                    self._walk(self._resolve_ref(ref))

            return

        if node_type.endswith("PictureItem"):
            self._walk_picture(node)
            return

        if node_type.endswith("TableItem"):
            self._walk_table(node)
            return

    def _walk_picture(
        self,
        picture,
    ):
        caption = ""

        for ref in picture.captions:
            node = self._resolve_ref(ref)

            if node is None:
                continue

            if hasattr(node, "text"):
                if caption:
                    caption += " "

                caption += node.text.strip()

        self._chunks.append(
            {
                "heading": self._current_heading,
                "type": "picture",
                "caption": caption,
                "picture": picture,
            }
        )

    def _walk_table(
        self,
        table,
    ):
        self._chunks.append(
            {
                "heading": self._current_heading,
                "type": "table",
                "table": table,
            }
        )

    def _resolve_ref(
        self,
        ref,
    ):
        cref = ref.cref

        if cref.startswith("#/texts/"):
            return self._document.texts[int(cref.split("/")[-1])]

        if cref.startswith("#/groups/"):
            return self._document.groups[int(cref.split("/")[-1])]

        if cref.startswith("#/pictures/"):
            return self._document.pictures[int(cref.split("/")[-1])]

        if cref.startswith("#/tables/"):
            return self._document.tables[int(cref.split("/")[-1])]

        return None

    def _flush(self):
        if not self._current_text:
            return

        text = "\n\n".join(
            self._current_text,
        )

        key = (
            self._current_heading,
            text,
        )

        if key in self._seen:
            self._current_text = []

            return

        self._seen.add(
            key,
        )

        self._chunks.append(
            {
                "heading": self._current_heading,
                "text": text,
            }
        )

        self._current_text = []

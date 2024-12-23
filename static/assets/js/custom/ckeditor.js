const {
  BalloonEditor,
  Alignment,
  Autoformat,
  AutoImage,
  AutoLink,
  Autosave,
  BalloonToolbar,
  Base64UploadAdapter,
  BlockQuote,
  Bold,
  Bookmark,
  CloudServices,
  Code,
  CodeBlock,
  Essentials,
  FindAndReplace,
  FontBackgroundColor,
  FontColor,
  FontFamily,
  FontSize,
  GeneralHtmlSupport,
  Heading,
  Highlight,
  HorizontalLine,
  HtmlComment,
  HtmlEmbed,
  ImageBlock,
  ImageCaption,
  ImageInline,
  ImageInsert,
  ImageInsertViaUrl,
  ImageResize,
  ImageStyle,
  ImageTextAlternative,
  ImageToolbar,
  ImageUpload,
  Indent,
  IndentBlock,
  Italic,
  Link,
  LinkImage,
  List,
  ListProperties,
  MediaEmbed,
  Paragraph,
  RemoveFormat,
  ShowBlocks,
  SpecialCharacters,
  SpecialCharactersArrows,
  SpecialCharactersCurrency,
  SpecialCharactersEssentials,
  SpecialCharactersLatin,
  SpecialCharactersMathematical,
  SpecialCharactersText,
  Strikethrough,
  Style,
  Subscript,
  Superscript,
  Table,
  TableCaption,
  TableCellProperties,
  TableColumnResize,
  TableProperties,
  TableToolbar,
  TextPartLanguage,
  TextTransformation,
  Title,
  TodoList,
  Underline,
  WordCount,
} = window.CKEDITOR;

/**
 * This is a 24-hour evaluation key. Create a free account to use CDN: https://portal.ckeditor.com/checkout?plan=free
 */
const LICENSE_KEY =
  "eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3NjY1MzQzOTksImp0aSI6IjRkNDdlZTVmLWJlOTMtNDM0ZS05ODJhLTUyMDUxNjZiYjE0MSIsInVzYWdlRW5kcG9pbnQiOiJodHRwczovL3Byb3h5LWV2ZW50LmNrZWRpdG9yLmNvbSIsImRpc3RyaWJ1dGlvbkNoYW5uZWwiOlsiY2xvdWQiLCJkcnVwYWwiXSwiZmVhdHVyZXMiOlsiRFJVUCJdLCJ2YyI6IjQ3ODBhMTYxIn0.ZfjkAfkLexfzAnaeaxXvc1Y9u-EMtswvC53JS-4oE1uQ9IUqpMDLtpnu978gNoh_QAUgI6hHlceNwY515G3h5A";

const editorConfig = {
  toolbar: {
    items: [
      "showBlocks",
      "findAndReplace",
      "textPartLanguage",
      "|",
      "heading",
      "style",
      "|",
      "fontSize",
      "fontFamily",
      "fontColor",
      "fontBackgroundColor",
      "|",
      "bold",
      "italic",
      "underline",
      "strikethrough",
      "subscript",
      "superscript",
      "code",
      "removeFormat",
      "|",
      "specialCharacters",
      "horizontalLine",
      "link",
      "bookmark",
      "insertImage",
      "mediaEmbed",
      "insertTable",
      "highlight",
      "blockQuote",
      "codeBlock",
      "htmlEmbed",
      "|",
      "alignment",
      "|",
      "bulletedList",
      "numberedList",
      "todoList",
      "outdent",
      "indent",
    ],
    shouldNotGroupWhenFull: false,
  },
  plugins: [
    Alignment,
    Autoformat,
    AutoImage,
    AutoLink,
    Autosave,
    BalloonToolbar,
    Base64UploadAdapter,
    BlockQuote,
    Bold,
    Bookmark,
    CloudServices,
    Code,
    CodeBlock,
    Essentials,
    FindAndReplace,
    FontBackgroundColor,
    FontColor,
    FontFamily,
    FontSize,
    GeneralHtmlSupport,
    Heading,
    Highlight,
    HorizontalLine,
    HtmlComment,
    HtmlEmbed,
    ImageBlock,
    ImageCaption,
    ImageInline,
    ImageInsert,
    ImageInsertViaUrl,
    ImageResize,
    ImageStyle,
    ImageTextAlternative,
    ImageToolbar,
    ImageUpload,
    Indent,
    IndentBlock,
    Italic,
    Link,
    LinkImage,
    List,
    ListProperties,
    MediaEmbed,
    Paragraph,
    RemoveFormat,
    ShowBlocks,
    SpecialCharacters,
    SpecialCharactersArrows,
    SpecialCharactersCurrency,
    SpecialCharactersEssentials,
    SpecialCharactersLatin,
    SpecialCharactersMathematical,
    SpecialCharactersText,
    Strikethrough,
    Style,
    Subscript,
    Superscript,
    Table,
    TableCaption,
    TableCellProperties,
    TableColumnResize,
    TableProperties,
    TableToolbar,
    TextPartLanguage,
    TextTransformation,
    Title,
    TodoList,
    Underline,
    WordCount,
  ],
  balloonToolbar: [
    "bold",
    "italic",
    "|",
    "link",
    "insertImage",
    "|",
    "bulletedList",
    "numberedList",
  ],
  fontFamily: {
    supportAllValues: true,
  },
  fontSize: {
    options: [10, 12, 14, "default", 18, 20, 22],
    supportAllValues: true,
  },
  heading: {
    options: [
      {
        model: "paragraph",
        title: "Paragraph",
        class: "ck-heading_paragraph",
      },
      {
        model: "heading1",
        view: "h1",
        title: "Heading 1",
        class: "ck-heading_heading1",
      },
      {
        model: "heading2",
        view: "h2",
        title: "Heading 2",
        class: "ck-heading_heading2",
      },
      {
        model: "heading3",
        view: "h3",
        title: "Heading 3",
        class: "ck-heading_heading3",
      },
      {
        model: "heading4",
        view: "h4",
        title: "Heading 4",
        class: "ck-heading_heading4",
      },
      {
        model: "heading5",
        view: "h5",
        title: "Heading 5",
        class: "ck-heading_heading5",
      },
      {
        model: "heading6",
        view: "h6",
        title: "Heading 6",
        class: "ck-heading_heading6",
      },
    ],
  },
  htmlSupport: {
    allow: [
      {
        name: "img",
        styles: true,
        attributes: {
          class: true,
        },
      },
      {
        name: "figure",
        attributes: {
          class: true,
        },
      },
      {
        name: /^.*$/,
        styles: true,
        attributes: true,
        classes: true,
      },
    ],
  },
  image: {
    toolbar: [
      "imageStyle:alignLeft",
      "imageStyle:alignCenter",
      "imageStyle:alignRight",
      "|",
      "toggleImageCaption",
      "imageTextAlternative",
    ],
  },
  initialData: document.getElementById("saved-content").innerHTML,
  language: "pt-br",
  licenseKey: LICENSE_KEY,
  link: {
    addTargetToExternalLinks: true,
    defaultProtocol: "https://",
    decorators: {
      toggleDownloadable: {
        mode: "manual",
        label: "Downloadable",
        attributes: {
          download: "file",
        },
      },
    },
  },
  list: {
    properties: {
      styles: true,
      startIndex: true,
      reversed: true,
    },
  },
  placeholder: "Type or paste your content here!",
  style: {
    definitions: [
      {
        name: "Article category",
        element: "h3",
        classes: ["category"],
      },
      {
        name: "Title",
        element: "h2",
        classes: ["document-title"],
      },
      {
        name: "Subtitle",
        element: "h3",
        classes: ["document-subtitle"],
      },
      {
        name: "Info box",
        element: "p",
        classes: ["info-box"],
      },
      {
        name: "Side quote",
        element: "blockquote",
        classes: ["side-quote"],
      },
      {
        name: "Marker",
        element: "span",
        classes: ["marker"],
      },
      {
        name: "Spoiler",
        element: "span",
        classes: ["spoiler"],
      },
      {
        name: "Code (dark)",
        element: "pre",
        classes: ["fancy-code", "fancy-code-dark"],
      },
      {
        name: "Code (bright)",
        element: "pre",
        classes: ["fancy-code", "fancy-code-bright"],
      },
    ],
  },
  table: {
    contentToolbar: [
      "tableColumn",
      "tableRow",
      "mergeTableCells",
      "tableProperties",
      "tableCellProperties",
    ],
  },
};

const editButton = document.getElementById("edit-button");
const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const contentView = document.getElementById("content-view");
const editorSection = document.getElementById("editor-section");
let editorInstance;
console.log(editButton);

BalloonEditor.create(document.querySelector("#editor"), editorConfig).then(
  (editor) => {
    editorInstance = editor;
    const wordCount = editor.plugins.get("WordCount");
    document
      .querySelector("#editor-word-count")
      .appendChild(wordCount.wordCountContainer);

    return editor;
  }
);

// Mostrar o editor ao clicar em "Editar" ou "Comece a Criar"
editButton.addEventListener("click", () => {
  contentView.classList.add("d-none");
  editorSection.classList.remove("d-none");
});

// Cancelar a edição
cancelButton.addEventListener("click", () => {
  editorSection.classList.add("d-none");
  contentView.classList.remove("d-none");
});

saveButton.addEventListener("click", async () => {
  const content = editorInstance.getData();
  console.log("Conteúdo gerado pelo editor:", content); // Adicione este log
  try {
    await saveContent(content);
    alert("Conteúdo salvo com sucesso!");
    location.reload();
  } catch (error) {
    alert("Erro ao salvar o conteúdo. Tente novamente.");
  }
});

// Função para salvar conteúdo no backend
async function saveContent(content) {
  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content }),
  });
  if (!response.ok) throw new Error("Erro ao salvar o conteúdo.");
}

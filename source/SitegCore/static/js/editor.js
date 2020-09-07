function modifyToken(token, modifyFn, env) {
    // create attrObj for convenient get/set of attributes
    var attrObj = (token.attrs) ? token.attrs.reduce(function (acc, pair) {
      acc[pair[0]] = pair[1];
      return acc;
    }, {}) : {};
    token.attrObj = attrObj;
    modifyFn(token, env);
    // apply any overrides or new attributes from attrObj
    Object.keys(token.attrObj).forEach(function (k) {
      token.attrSet(k, token.attrObj[k]);
    });
}

const tm = texmath.use(katex);
var md = window.markdownit({
    typographer: true
}).use(window.markdownitEmoji);
md.use(window.markdownitDeflist);
md.use(tm, { engine: katex,
    delimiters:'dollars',
    katexOptions: { macros: {"\\RR": "\\mathbb{R}"} }
  });

prism = window.prismjs

md.renderer.rules.emoji = function(token, idx) {
    return twemoji.parse(token[idx].content);
};

var editor = ace.edit("editor");

md.core.ruler.push('modify-token', function (state) {
        var modifyFn = md.options.modifyToken;
        state.tokens.forEach(function (token) {
        if (token.children && token.children.length) {
            token.children.forEach(function (token) {
            modifyToken(token, modifyFn, state.env);
            });
        }
        modifyToken(token, modifyFn, state.env);
        });
        return false;
});


editor.setTheme("ace/theme/textmate");
editor.session.setMode("ace/mode/markdown");
document.getElementById('editor').style.fontSize = '14px';
editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    showPrintMargin: false,
});

// Key Bindings
editor.commands.addCommand({ 
    name: 'bold', 
    bindKey: { win: 'Ctrl-B', mac: 'Command-B' },
    exec: function (editor) {
        editor.insertSnippet('**${1:$SELECTION}**');
    },
    readOnly: false
});
editor.commands.addCommand({
    name: 'italic',
    bindKey: { win: 'Ctrl-I', mac: 'Command-I' },
    exec: function (editor) {
        editor.insertSnippet('*${1:$SELECTION}*');
    },
    readOnly: false
});
editor.commands.addCommand({
    name: 'strike',
    bindKey: { win: 'Ctrl-U', mac: 'Command-U' },
    exec: function (editor) {
        editor.insertSnippet('~~${1:$SELECTION}~~');
    },
    readOnly: false
});
editor.commands.addCommand({
    name: 'save',
    bindKey: { win: 'Ctrl-S', mac: 'Command-S' },
    exec: function (editor) {
        saveMD();
    },
    readOnly: false
});

editor.session.setUseWrapMode(true);
editor.container.style.lineHeight = 2;

// Markdown Highlighting Code
md.set({
    highlight: function (str, lang) {
        let hl
        try {
        hl = Prism.highlight(str, Prism.languages[lang])
        } catch (error) {
        hl = md.utils.escapeHtml(str)
        }
        return `<pre class="language-${lang} rounded mr-2"><code class="language-${lang}">${hl}</code></pre>`
    }
})

// Markdown adding attributes to html tags
md.set({
    modifyToken: function (token, env) {
        switch (token.tag) {
            case 'img': 
                if (token.attrObj.class != 'emoji') {
                    token.attrObj.class = 'img-fluid'; 
                }
                break;
            case 'table':
                token.attrObj.class = 'table table-hover'; 
                break;
            case 'dd':
                token.attrObj.class = 'ml-2'; 
                break;
            case 'dl':
                token.attrObj.class = 'border rounded px-2'; 
                break;
            case 'blockquote':
                token.attrObj.class = 'blockquote pl-2 py-1'; 
                token.attrObj.style = 'border-left: 5px solid #eee;'; 
                break;
            case 'h2':
                token.attrObj.class = "mb-3 mt-5 toc-h2";
                break;
            case 'h3':
                token.attrObj.class = "mb-3 mt-5 toc-h3";
                break;
        }
    }
})

// document on ready
$(document).ready(function () {
    var value = $('input[type=checkbox]').prop("checked");
    var name = $('input[type=checkbox]').attr("name");
    switch (name) {
        case "html":
            md.set({
                html: value,
            });
            break;
        case "auto-link":
            md.set({
                linkify: value
            });;
            break;
        case "break":
            md.set({
                breaks: value
            });;
            break;
    }
    resetPreview();
    $('#toggle-preview').children('.fa-eye').hide();
    $('#preview1').hide();
    $('.unsaved').hide();
});

editor.session.on('change', function(delta) {
    resetPreview();
    $('.unsaved').show();
});

editor.renderer.on('afterRender', function() {
    resetPreview();
});

$('input[type=checkbox]').change(function (e) { 
    e.preventDefault();

    var value = $(e.target).prop("checked");
    var name = $(e.target).attr("name");
    switch (name) {
        case "html":
            md.set({
                html: value,
            });
            break;
        case "auto-link":
            md.set({
                linkify: value
            });;
            break;
        case "break":
            md.set({
                breaks: value
            });;
            break;
    }
    resetPreview();

    var formData = new FormData();
    formData.append('html', $('#editor-form').find('input[name=html]').prop("checked"));
    formData.append('breakC', $('#editor-form').find('input[name=break]').prop("checked"));
    formData.append('autoLink', $('#editor-form').find('input[name=auto-link]').prop("checked"));
    formData.append("submit", "setup-md");
    $.ajax({
        type: "post",
        url: document.location.href,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {}
    });
});

/* Submit markdown */
$('#save-md').click(function (e) { 
    e.preventDefault();
    saveMD();
});

$('#toggle-preview').click(function (e) { 
    e.preventDefault();
    $('#toggle-preview').children('.fa-eye').toggle();
    $('#toggle-preview').children('.fa-code').toggle();
    $('#preview-htm').toggle();
    $('#preview1').toggle();
});

function resetPreview() {
    var result = md.render(editor.getValue());
    $("#preview-htm").html(result);
    $("#preview1").text($('#preview-htm').html());
    $(".img-fluid").wrap('<p class="hover-img"></p>');
}

function saveMD() {
    var formData = new FormData();

    formData.append('mdData', editor.getValue());
    formData.append('htmlData', $('#preview-htm').html());
    formData.append('submit', "save-md");
    $.ajax({
        type: "post",
        url: document.location.href,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $('.unsaved').hide();
        }
    });
}


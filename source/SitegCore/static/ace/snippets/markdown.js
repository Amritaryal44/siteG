define("ace/snippets/markdown",["require","exports","module"], function(require, exports, module) {
"use strict";

exports.snippetText = "# Markdown\n\
\n\
snippet linkexternal\n\
	[${1:text}](http://${2:address} \"${3:title}\")\n\
snippet linkexternal\n\
	[${1:text}](http://${2:address} \"${3:title}\")\n\
snippet linkinternal\n\
	[${1:text}](${2:internal-url} \"${3:title}\")${4}\n\
\n\
snippet linkdirect\n\
	<http://${1:url}>\n\
\n\
snippet linkid\n\
	[${1:name}][${2:id}]\n\n\
\n\
snippet imgid\n\
	![${1:name}][${2:id}]\n\n\
\n\
snippet img\n\
	![${1:alttext}](/posts/images/${2:post-id}/${2:post-id}-${3:image-id}.jpg \"${4:title}\")\n\
\n\
snippet id\n\
	[${2:id}]: ${3:external-url} \"${4:title}\"\n\
\n\
snippet blockquote\n\
	> ${1:blockquote}\n\
\n\
snippet codel\n\
	```\n\
	${1:code}\n\
	```\n\
\n\
snippet codes\n\
	`${1:inline-code}`\n\
\n\
snippet def\n\
	${1:definition_title}\n\
	: ${2:definition_title}\n\
\n\
snippet yt-img\n\
	[![${1:Image_alt}](http://img.youtube.com/vi/${2}/0.jpg)](http://www.youtube.com/watch?v=${2:yt_id} \"${3:title}\")\n\
\n\
";
exports.scope = "markdown";

});                (function() {
                    window.require(["ace/snippets/markdown"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            

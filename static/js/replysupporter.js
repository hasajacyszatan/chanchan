const zawartosci = document.querySelectorAll(".postcontent");

for (const el of zawartosci) {
    const matches = el.textContent.match(/>>\d+/g);
    if (!matches) continue;

    const unique = [...new Set(matches)];
    let html = el.innerHTML;

    for (const ref of unique) {
        const id = ref.replace(">>", "");
        const encoded = ref.replaceAll(">", "&gt;"); // &gt;&gt;123
        html = html.replaceAll(encoded, `<a href="#r${id}">${ref}</a>`);
    }

    el.innerHTML = html;
    console.log(el.innerHTML);
}

function replytoreply(replyid) {
	replytext.innerHTML = replytext.innerHTML+">>"+replyid
}
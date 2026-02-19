(function() {
    var quotes = [
        { text: "代码是写给人看的，顺便给机器执行。", author: "Donald Knuth" },
        { text: "简单是可靠的先决条件。", author: "Edsger Dijkstra" },
        { text: "过早优化是万恶之源。", author: "Donald Knuth" },
        { text: "程序必须是为了给人看而写，给机器执行只是附带任务。", author: "Donald Knuth" },
        { text: "好的代码本身就是最好的文档。", author: "Steve McConnell" },
        { text: "先让它工作，再让它正确，最后让它快。", author: "Kent Beck" },
        { text: "任何傻瓜都能写出计算机能理解的代码，优秀的程序员写出人能理解的代码。", author: "Martin Fowler" },
        { text: "编程不是关于你知道什么，而是关于你能想出什么。", author: "Chris Pine" },
        { text: "最好的代码是没有代码。", author: "Jeff Atwood" },
        { text: "调试比编写代码难两倍，所以如果你写代码时用尽了聪明才智，从定义上讲，你就没有足够的智慧去调试它。", author: "Brian Kernighan" },
        { text: "谈技术不如谈生活，谈生活不如谈技术。", author: "佚名" },
        { text: "代码写的越少，Bug 越少。", author: "佚名" },
        { text: "保持学习，保持好奇。", author: "佚名" },
        { text: "今日事，今日毕。", author: "曾国藩" },
        { text: "三人行，必有我师焉。", author: "孔子" }
    ];
    
    var randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    var taglineElement = document.querySelector('meta[name="description"]');
    
    if (taglineElement) {
        taglineElement.setAttribute('content', randomQuote.text + ' — ' + randomQuote.author);
    }
    
    var siteDescription = document.querySelector('.site-subtitle, #sidebar .site-subtitle, .sidebar .site-subtitle');
    if (siteDescription) {
        siteDescription.textContent = randomQuote.text;
    }
})();

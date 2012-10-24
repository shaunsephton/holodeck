input = phantom.args[0];
output = phantom.args[1];
width = 620;
height = 240;

var page = new WebPage();
page.viewportSize = { width: width, height: height };
page.clipRect = { width: width, height: height };

page.open(input, function (status) {
    if (status !== 'success') {
        phantom.exit(1);
    }
    else {
        setTimeout(function() {
            page.render(output);
            phantom.exit();
        }, 200);
    }
});

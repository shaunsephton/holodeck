input = phantom.args[0];
output = phantom.args[1];
width = 300;
height = 240;

var page = new WebPage();
page.viewportSize = { width: width, height: height };
page.clipRect = { width: width, height: height };

page.open(input, function (status) {
    if (status !== 'success') {
        phantom.exit(1);
    }
    else {
        page.render(output);
        phantom.exit();
    }
});

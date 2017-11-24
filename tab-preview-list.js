var Custom = (function() {

var j_HTML = $('html');

function setTooltipPosition(wrapper, x1, y1, w1, h1) {
    var tooltip = wrapper.find('.tooltip');
    var w2 = tooltip.width();

    // Because macOS puts topbar buttons on left side...
    var contain = $('#tabs-container');
    var offset = parseInt(contain.css('padding-left'));

    var x2 = x1 - ((w2-w1)/2) + offset;
    var y2 = y1 + h1;

    if (x2 < 0)
        x2 = 0;
    if (x2 + w2 > j_HTML.width())
        x2 = j_HTML.width() - w2;

    //console.log("left: " + x2 + "\ntop: " + y2);

    tooltip.css({'left': x2 + 'px', 'top': y2 + 'px', 'padding-left': 0, 'padding-top': 0});
    wrapper.css({'visibility': 'visible'});

    //console.log("did custom event code");
}

j_HTML.on('mouseenter', '.tab-position', function() {
    //console.log("doing custom event code");    
    var tab = $(this);
    var wrapper = $('#vivaldi-tooltip');

    wrapper.css({'visibility': 'hidden'});

    var x1 = tab.position().left;
    var y1 = tab.position().top;

    var h1 = tab.height();
    var w1 = tab.width();

    var observer = new MutationObserver(function(mutations, observer) {
        setTimeout(setTooltipPosition, 100, wrapper, x1, y1, w1, h1);
        observer.disconnect();
    })

    observer.observe(document.getElementById('vivaldi-tooltip'), {
        subtree: true,
        attributes: true,
        childList: true
    })
})

})();
(function () {
  var icons = Array.prototype.slice.call(document.querySelectorAll('.cluster-icon'));
  var clusters = Array.prototype.slice.call(document.querySelectorAll('.doodle-cluster'));
  var baseClusterW = 400;
  var baseClusterH = 380;
  var SIZE = 1.53;
  var SPREAD = 3;

  function apply(scale, spread) {
    var clusterGrow = 1 + spread * 0.9;
    clusters.forEach(function (cluster) {
      cluster.style.width = (baseClusterW * clusterGrow) + 'px';
      cluster.style.height = (baseClusterH * clusterGrow) + 'px';
    });
    icons.forEach(function (icon) {
      if (icon.dataset.locked) return;
      var width = parseFloat(icon.dataset.baseWidth);
      var right = parseFloat(icon.dataset.baseRight);
      var vertProp, vertVal;
      if (icon.dataset.baseTop !== undefined) {
        vertProp = 'top';
        vertVal = parseFloat(icon.dataset.baseTop);
      } else {
        vertProp = 'bottom';
        vertVal = parseFloat(icon.dataset.baseBottom);
      }
      var newWidth = width * scale;
      var newRight = right * (1 + spread);
      var newVert = vertVal * (1 + spread);
      icon.style.width = newWidth + 'px';
      icon.style.right = newRight + 'px';
      icon.style[vertProp] = newVert + 'px';
    });
  }

  function hideOverlapping() {
    var boxes = Array.prototype.slice.call(
      document.querySelectorAll('.stage:not([hidden]) .stage-panel, .stage:not([hidden]) .doc-anim, .results-screen:not([hidden]) .card')
    ).map(function (b) { return b.getBoundingClientRect(); })
      .filter(function (r) { return r.width > 0 && r.height > 0; });
    if (!boxes.length) {
      icons.forEach(function (icon) { icon.style.opacity = ''; });
      return;
    }
    icons.forEach(function (icon) {
      var r = icon.getBoundingClientRect();
      var overlaps = boxes.some(function (box) {
        return !(r.right < box.left || r.left > box.right || r.bottom < box.top || r.top > box.bottom);
      });
      icon.style.opacity = overlaps ? '0' : '';
    });
  }

  apply(SIZE, SPREAD);
  requestAnimationFrame(function () {
    requestAnimationFrame(hideOverlapping);
  });
  setTimeout(hideOverlapping, 300);
  window.addEventListener('load', hideOverlapping);
  window.addEventListener('resize', hideOverlapping);
  var appMain = document.querySelector('.app-main');
  if (appMain) {
    new MutationObserver(function () { requestAnimationFrame(hideOverlapping); })
      .observe(appMain, { attributes: true, attributeFilter: ['hidden'], subtree: true });
  }
})();

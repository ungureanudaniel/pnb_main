module.exports = {
  content: ['./**/templates/**/*.html'],
  css: ['./static/css/styles.min.css'],
  output: './static/csspurged/',
  safelist: {
    standard: [
      /slick-/, /fancybox-/, /irs-/, /r-tabs-/, /nice-select/,
      'modal', 'modal-open', 'show', 'active', 'fade', 'in',
      'alert-success', 'alert-info', 'alert-warning', 'alert-danger',
      'toast', 'toast-*'
    ]
  }
};
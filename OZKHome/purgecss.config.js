module.exports = {
  content: [
    './**/*.html',         // all your HTML files
    './**/*.js',           // if classes are toggled in JS
  ],
  css: ['./style.css'],     // your main CSS file
  safelist: [
    // Keep anything generated dynamically or by JS/Tailwind variants
    // Examples—tweak for your project:
    /^bg-/, /^text-/, /^border-/, /^hover:/, /^focus:/,
    /^md:/, /^lg:/, /^xl:/,
    'hidden', 'open', 'active', 'is-open', 'is-visible',
  ],
}

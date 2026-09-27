(() => {
  'use strict';
  if (!('IntersectionObserver' in window) || !Element.prototype.animate ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const cardName = /(?:^|[-_])(?:card|tile)(?:s)?(?:$|[-_])|(?:Card|Tile)$/;
  const excluded = 'header, nav, footer, form, [role="navigation"], [aria-hidden="true"]';
  const root = document.querySelector('main, [role="main"]') || document.body;
  const candidates = Array.from(root.querySelectorAll('[class], article')).filter((element) => {
    if (element.closest(excluded) || element.classList.contains('reveal')) return false;
    const names = Array.from(element.classList);
    const named = names.some((name) => cardName.test(name));
    const gridArticle = element.tagName === 'ARTICLE' &&
      /grid|cards|tiles|list/i.test(element.parentElement?.className || '');
    if (!named && !gridArticle) return false;
    if (names.some((name) => /(?:^|[-_])(?:grid|list|wrap|container)(?:$|[-_])|(?:Grid|List|Wrap)$/.test(name))) return false;
    const style = getComputedStyle(element);
    return style.display !== 'none' && style.visibility !== 'hidden' &&
      style.position !== 'fixed' && style.position !== 'sticky' &&
      element.getBoundingClientRect().height >= 40;
  });
  const cards = candidates.filter((element) =>
    !candidates.some((other) => other !== element && other.contains(element)));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (!isIntersecting) return;
      observer.unobserve(target);
      target.animate([
        { opacity: 0, transform: 'translateY(14px)' },
        { opacity: 1, transform: 'translateY(0)' }
      ], { duration: 700, easing: 'ease-out' });
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
  cards.forEach((card) => observer.observe(card));
})();

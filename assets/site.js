const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-navigation');
menuToggle?.addEventListener('click', () => {
  const expanded = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(expanded));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuToggle?.getAttribute('aria-expanded') === 'true') {
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.focus();
  }
});
document.querySelector('#print-cv')?.addEventListener('click',()=>window.print());
if(document.body.classList.contains('cv-page')) document.querySelectorAll('details').forEach(d=>d.open=true);
const legacyPages={research:'research.html',publications:'papers.html',experience:'experience.html',teaching:'teaching.html',education:'education.html',awards:'awards.html',leadership:'beyond-research.html'};
if(document.body.classList.contains('page-about') && legacyPages[location.hash.slice(1)]) location.replace(legacyPages[location.hash.slice(1)]);

const bandLinks = [...document.querySelectorAll('.band-photo')];
const bandDialog = document.querySelector('.band-lightbox');
if (bandDialog && typeof bandDialog.showModal === 'function') {
  let bandIndex = 0;
  let bandOpener;
  const fullImageCache = new Map();
  const fullImage = bandDialog.querySelector('.band-full');
  const count = bandDialog.querySelector('.band-count');
  const preloadBandPhoto = index => {
    const normalizedIndex = (index + bandLinks.length) % bandLinks.length;
    if (!fullImageCache.has(normalizedIndex)) {
      const image = new Image();
      const loaded = new Promise(resolve => {
        image.onload = () => resolve(image);
        image.onerror = () => resolve(null);
      });
      image.src = bandLinks[normalizedIndex].href;
      fullImageCache.set(normalizedIndex, loaded);
    }
    return fullImageCache.get(normalizedIndex);
  };
  const showBandPhoto = index => {
    bandIndex = (index + bandLinks.length) % bandLinks.length;
    const source = bandLinks[bandIndex].querySelector('img');
    const requestedIndex = bandIndex;
    fullImage.src = source.currentSrc || source.src;
    fullImage.alt = source.alt;
    count.textContent = `${bandIndex + 1} / ${bandLinks.length}`;
    preloadBandPhoto(bandIndex).then(image => {
      if (image && bandIndex === requestedIndex) fullImage.src = image.src;
    });
  };
  bandLinks.forEach((link, index) => {
    link.addEventListener('pointerenter', () => preloadBandPhoto(index), {once:true});
    link.addEventListener('focus', () => preloadBandPhoto(index), {once:true});
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      bandOpener = link;
      showBandPhoto(index);
      bandDialog.showModal();
      document.documentElement.classList.add('band-viewing');
      bandDialog.querySelector('.band-close').focus();
    });
  });
  bandDialog.querySelector('.band-close').addEventListener('click', () => bandDialog.close());
  bandDialog.querySelector('.band-prev').addEventListener('click', () => showBandPhoto(bandIndex - 1));
  bandDialog.querySelector('.band-next').addEventListener('click', () => showBandPhoto(bandIndex + 1));
  bandDialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      showBandPhoto(bandIndex + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  bandDialog.addEventListener('click', event => { if (event.target === bandDialog) bandDialog.close(); });
  bandDialog.addEventListener('close', () => {
    document.documentElement.classList.remove('band-viewing');
    bandOpener?.focus({preventScroll:true});
  });
}


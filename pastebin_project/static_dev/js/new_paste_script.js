const tiredElements = document.getElementsByClassName('new-paste-line');
for (const element of tiredElements) {
  element.addEventListener('mouseenter', () => {
    element.style.backgroundColor = '#620eaf';
    element.style.padding = '11px';
  });

  element.addEventListener('mouseleave', () => {
    element.style.backgroundColor = '';
    element.style.padding = '0px';
  });
}
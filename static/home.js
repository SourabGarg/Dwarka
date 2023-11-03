function imgSlider(imageSrc, bgColor, newTitle, newText, newPara, newLink, newValue, setectedValue) {
  // Change the image source and background color
  document.querySelector('.svg-image').src = imageSrc;
  document.querySelector('.sec').style.backgroundColor = bgColor;
  
  // Change the text content
  
  document.querySelector('.text p').textContent = newPara;
  document.querySelector('.text h2').textContent = newTitle;
  document.querySelector('.text span').textContent = newText;
  
  var showMoreLink = document.getElementById('showMoreLink');
  showMoreLink.setAttribute('href', newLink);
  showMoreLink.setAttribute('value', newValue);

  var showMoreLink = document.getElementById('selected_data');
  showMoreLink.setAttribute('value', setectedValue);


}

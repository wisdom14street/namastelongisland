/* Namaste Long Island forms: delivered by FormSubmit (AJAX) to the inbox; GA4 generate_lead on success.
   If the request fails, the visitor gets a ready-to-send email instead, so nothing is lost. */
(function(){
  function ga(n,p){try{if(typeof window.gtag==='function')window.gtag('event',n,p||{})}catch(_){}}
  var cfg=window.NLI||{};
  // prefill category from ?category=
  try{var c=new URLSearchParams(location.search).get('category');var s=document.getElementById('f-category');
    if(c&&s){var m={wedding:'Wedding: venue',venues:'Wedding: venue',catering:'Wedding: caterer',decor:'Wedding: decor',dj:'Wedding: DJ',photo:'Wedding: photo',mehndi:'Wedding: mehndi',makeup:'Wedding: hair',attire:'Wedding: attire',jewelry:'Wedding: jeweler',priests:'Wedding: pandit',cards:'Wedding: invitations',planners:'Wedding: planner',restaurant:'Restaurant',restaurants:'Restaurant',sweets:'Sweets',chaat:'Chaat',tiffin:'Tiffin',shop:'Clothing',puja:'Puja',community:'Temple'}[c];
      if(m)[].some.call(s.options,function(o){if(o.text.indexOf(m)===0){s.value=o.text;return true}})}}catch(_){}
  function collect(box){var d={};[].forEach.call(box.querySelectorAll('input,select,textarea'),function(el){
    if(!el.name)return;if(el.type==='checkbox'){d[el.name]=el.checked?'yes':'no';return}d[el.name]=(el.value||'').trim()});return d}
  function valid(box){var els=box.querySelectorAll('input,select,textarea');for(var i=0;i<els.length;i++){var el=els[i];
    if(el.checkValidity&&!el.checkValidity()){el.reportValidity&&el.reportValidity();el.focus();return false}}return true}
  function mailto(subj,d){var body=Object.keys(d).filter(function(k){return k[0]!=='_'}).map(function(k){return k+': '+d[k]}).join('\n');
    return 'mailto:'+cfg.email+'?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(body)}
  [].forEach.call(document.querySelectorAll('[data-form]'),function(box){
    var btn=box.querySelector('.send'),msg=box.querySelector('.msg'),kind=box.getAttribute('data-form');
    function go(e){if(e)e.preventDefault();if(btn.disabled||!valid(box))return;
      var d=collect(box);if(d._honey){msg.textContent='Thanks!';return}
      var subj=(box.getAttribute('data-subject')||'Form')+(d.business?': '+d.business:d.event_name?': '+d.event_name:d.email?': '+d.email:'');
      d._subject='[Namaste Long Island] '+subj;d._template='table';d._captcha='false';d.form=kind;d.page=location.href;
      btn.disabled=true;msg.className='msg';msg.textContent='Sending...';
      fetch(cfg.endpoint,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(d)})
      .then(function(r){return r.json().catch(function(){return{}}).then(function(j){if(!r.ok||String(j.success)==='false')throw new Error(j.message||r.status);return j})})
      .then(function(){ga('generate_lead',{form_type:kind,lead_source:'form'});msg.className='msg ok';
        msg.textContent=kind==='newsletter'?'You\'re on the list. Thank you!':'Thank you! We\'ll be in touch by email soon.';
        [].forEach.call(box.querySelectorAll('input:not([type=hidden]):not([type=checkbox]),textarea'),function(el){el.value=''})})
      .catch(function(){msg.className='msg err';msg.innerHTML='We couldn\'t send that just now. <a href="'+mailto(subj,d)+'">Email it to us instead</a> and we\'ll take it from there.';
        ga('form_error',{form_type:kind})})
      .then(function(){btn.disabled=false})}
    btn.addEventListener('click',go);
    box.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.tagName==='INPUT'&&e.target.type!=='checkbox')go(e)});
  });
  // generate_lead on phone / email / directions taps
  document.addEventListener('click',function(e){try{var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'',k='';
    if(/^tel:/i.test(h))k='phone';else if(/^mailto:/i.test(h))k='email';else if(/google\.[a-z.]+\/maps/i.test(h))k='directions';
    if(k)ga('generate_lead',{link_type:k,link_url:h.slice(0,200),transport_type:'beacon'})}catch(_){}},true);
})();

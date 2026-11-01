/* Namaste Long Island forms: delivered by FormSubmit (AJAX) to the inbox; GA4 generate_lead on success.
   If the request fails, the visitor gets a ready-to-send email instead, so nothing is lost. */
(function(){
  function ga(n,p){try{if(typeof window.gtag==='function')window.gtag('event',n,p||{})}catch(_){}}
  var cfg=window.NLI||{};
  // prefill category from ?category=
  try{var c=new URLSearchParams(location.search).get('category');var s=document.getElementById('f-category');
    if(c&&s){var m={wedding:'Wedding: venue',venues:'Wedding: venue',catering:'Wedding: caterer',decor:'Wedding: decor',dj:'Wedding: DJ',photo:'Wedding: photo',mehndi:'Wedding: mehndi',makeup:'Wedding: hair',attire:'Wedding: attire',jewelry:'Wedding: jeweler',priests:'Wedding: pandit',cards:'Wedding: invitations',planners:'Wedding: planner',restaurant:'Restaurant',restaurants:'Restaurant',sweets:'Sweets',chaat:'Chaat',tiffin:'Tiffin',shop:'Clothing',puja:'Puja',community:'Temple'}[c];
      if(m)[].some.call(s.options,function(o){if(o.text.indexOf(m)===0){s.value=o.text;return true}})}}catch(_){}
  // prefill listing from ?listing=
  try{var li=new URLSearchParams(location.search).get('listing');if(li){var f=document.getElementById('f-listing')||document.getElementById('f-listing_url');if(f)f.value=location.origin+'/directory/#'+li;var b=document.getElementById('f-business');if(b&&!b.value)b.value=li.replace(/-/g,' ')}}catch(_){}
  // directory search / filter
  (function(){var q=document.getElementById('dq');if(!q)return;var t=document.getElementById('dt'),cards=[].slice.call(document.querySelectorAll('.lst')),secs=[].slice.call(document.querySelectorAll('.dsec')),chips=[].slice.call(document.querySelectorAll('.chip')),cnt=document.getElementById('dcount'),none=document.getElementById('dnone'),cat='',tm;
    function run(){var v=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean),tv=t?t.value:'',n=0;
      cards.forEach(function(c){var ok=(!cat||c.dataset.cat===cat)&&(!tv||c.dataset.town===tv)&&v.every(function(w){return c.dataset.q.indexOf(w)>-1});c.hidden=!ok;if(ok)n++});
      secs.forEach(function(s){s.hidden=!s.querySelector('.lst:not([hidden])')});
      if(cnt)cnt.textContent=(v.length||tv||cat)?n+' match'+(n===1?'':'es'):'';if(none)none.hidden=n>0;
      clearTimeout(tm);if(v.length)tm=setTimeout(function(){ga('search',{search_term:q.value.slice(0,80)})},1200)}
    q.addEventListener('input',run);if(t)t.addEventListener('change',run);
    chips.forEach(function(ch){ch.addEventListener('click',function(){chips.forEach(function(x){x.classList.remove('on')});ch.classList.add('on');cat=ch.dataset.f;run()})});
    var sp=new URLSearchParams(location.search),h=sp.get('q'),tw=sp.get('town'),cf=sp.get('cat');if(h)q.value=h;if(tw&&t)t.value=tw;
    if(cf)chips.forEach(function(ch){if(ch.dataset.f===cf){chips.forEach(function(x){x.classList.remove('on')});ch.classList.add('on');cat=cf}});if(h||tw||cf)run()})();
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-ev]');if(!a)return;var c=a.closest('.lst');
    try{ga('listing_'+a.dataset.ev,{listing:c?c.id:'',category:c?c.dataset.cat:''})}catch(_){}});
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

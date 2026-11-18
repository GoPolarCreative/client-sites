/**
 * Go Polar instant enquiry auto-reply.
 *
 * Deployed as a Google Apps Script web app on the Go Polar Gmail account
 * (Execute as: me, Who has access: Anyone). Client sites POST each enquiry here
 * after Web3Forms accepts it. The reply goes out in the client's business name,
 * with Reply-To set to the client's own email, so any reply lands with them.
 *
 * Which sites may use it, and what they say, comes from autoreply.json in the
 * public client-sites repo. Only sites listed there with "enabled": true get
 * replies. The customer's message is never echoed back, so this cannot be used
 * to relay arbitrary text.
 */
var CONFIG_URL = 'https://raw.githubusercontent.com/GoPolarCreative/client-sites/main/autoreply.json';
var EMAIL_RE = /^[^\s@<>"]+@[^\s@<>"]+\.[A-Za-z]{2,}$/;

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var cfg = getConfig_()[String(d.site || '')];
    if (!cfg || !cfg.enabled) return out_('skip');
    var email = String(d.email || '').trim().slice(0, 120);
    if (!EMAIL_RE.test(email)) return out_('no-email');

    // One auto-reply per address per site every 6 hours, and keep quota in reserve.
    var cache = CacheService.getScriptCache();
    var key = 'ar:' + d.site + ':' + email.toLowerCase();
    if (cache.get(key)) return out_('duplicate');
    if (MailApp.getRemainingDailyQuota() < 5) return out_('quota');

    var first = String(d.name || '').trim().split(/\s+/)[0].replace(/[^A-Za-z'\-]/g, '').slice(0, 30);
    var hi = first ? 'Hi ' + first + ',' : 'Hi there,';
    var who = cfg.owner || 'The team';
    var lines = [
      hi,
      '',
      'Thanks for getting in touch with ' + cfg.business + '. Your enquiry has come through.',
      '',
      who + ' is ' + (cfg.on_job || 'on the job') + ' right now and will get back to you as soon as possible.',
      '',
      cfg.phone ? 'If it is urgent, call ' + cfg.phone + '.' : '',
      '',
      cfg.business,
      cfg.phone || '',
      cfg.website || ''
    ];
    var text = lines.join('\n').replace(/\n{3,}/g, '\n\n');
    var html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#1a1a1a">' +
      '<p>' + esc_(hi) + '</p>' +
      '<p>Thanks for getting in touch with <strong>' + esc_(cfg.business) + '</strong>. Your enquiry has come through.</p>' +
      '<p>' + esc_(who) + ' is ' + esc_(cfg.on_job || 'on the job') + ' right now and will get back to you as soon as possible.</p>' +
      (cfg.phone ? '<p>If it is urgent, call <a href="tel:' + esc_(cfg.tel || cfg.phone) + '">' + esc_(cfg.phone) + '</a>.</p>' : '') +
      '<p style="margin-top:24px">' + esc_(cfg.business) + (cfg.phone ? '<br>' + esc_(cfg.phone) : '') +
      (cfg.website ? '<br><a href="' + esc_(cfg.website) + '">' + esc_(cfg.website.replace(/^https?:\/\//, '')) + '</a>' : '') + '</p></div>';

    MailApp.sendEmail({
      to: email,
      subject: cfg.business + ': we have your enquiry',
      body: text,
      htmlBody: html,
      name: cfg.business,
      replyTo: cfg.reply_to
    });
    cache.put(key, '1', 21600);
    return out_('sent');
  } catch (err) {
    console.error(err);
    return out_('error');
  }
}

function doGet() {
  return out_('Go Polar auto-reply is running. Quota left today: ' + MailApp.getRemainingDailyQuota());
}

function getConfig_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get('config');
  if (hit) return JSON.parse(hit);
  var res = UrlFetchApp.fetch(CONFIG_URL, { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) return {};
  var body = res.getContentText();
  cache.put('config', body, 600);
  return JSON.parse(body);
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function out_(msg) {
  return ContentService.createTextOutput(msg);
}

/** Run once from the editor to approve permissions and send yourself a sample. */
function testToMe() {
  var me = Session.getEffectiveUser().getEmail();
  var res = doPost({ postData: { contents: JSON.stringify({ site: 'metrowide-plumbing', name: 'Chris Test', email: me }) } });
  Logger.log(res.getContent());
}

import re
from datetime import datetime, timezone

import bs4
from bs4 import BeautifulSoup
from functional import seq

html = """<html lang="en" op="news" data-darkreader-mode="dynamic" data-darkreader-scheme="dark" data-darkreader-proxy-injected="true"><head><style class="darkreader darkreader--fallback" media="screen"></style><style class="darkreader darkreader--text" media="screen"></style><style class="darkreader darkreader--invert" media="screen">.jfk-bubble.gtx-bubble, .captcheck_answer_label > input + img, span#closed_text > img[src^="https://www.gstatic.com/images/branding/googlelogo"], span[data-href^="https://www.hcaptcha.com/"] > #icon, img.Wirisformula, .votearrow {
    filter: invert(100%) hue-rotate(180deg) contrast(65%) sepia(15%) !important;
}</style><style class="darkreader darkreader--inline" media="screen">[data-darkreader-inline-bgcolor] {
  background-color: var(--darkreader-inline-bgcolor) !important;
}
[data-darkreader-inline-bgimage] {
  background-image: var(--darkreader-inline-bgimage) !important;
}
[data-darkreader-inline-border] {
  border-color: var(--darkreader-inline-border) !important;
}
[data-darkreader-inline-border-bottom] {
  border-bottom-color: var(--darkreader-inline-border-bottom) !important;
}
[data-darkreader-inline-border-left] {
  border-left-color: var(--darkreader-inline-border-left) !important;
}
[data-darkreader-inline-border-right] {
  border-right-color: var(--darkreader-inline-border-right) !important;
}
[data-darkreader-inline-border-top] {
  border-top-color: var(--darkreader-inline-border-top) !important;
}
[data-darkreader-inline-boxshadow] {
  box-shadow: var(--darkreader-inline-boxshadow) !important;
}
[data-darkreader-inline-color] {
  color: var(--darkreader-inline-color) !important;
}
[data-darkreader-inline-fill] {
  fill: var(--darkreader-inline-fill) !important;
}
[data-darkreader-inline-stroke] {
  stroke: var(--darkreader-inline-stroke) !important;
}
[data-darkreader-inline-outline] {
  outline-color: var(--darkreader-inline-outline) !important;
}
[data-darkreader-inline-stopcolor] {
  stop-color: var(--darkreader-inline-stopcolor) !important;
}
[data-darkreader-inline-bg] {
  background: var(--darkreader-inline-bg) !important;
}
[data-darkreader-inline-invert] {
    filter: invert(100%) hue-rotate(180deg);
}</style><style class="darkreader darkreader--variables" media="screen">:root {
   --darkreader-neutral-background: #353533;
   --darkreader-neutral-text: #d8d3c9;
   --darkreader-selection-background: #2c5b93;
   --darkreader-selection-text: #d8d3c9;
}</style><style class="darkreader darkreader--root-vars" media="screen"></style><style class="darkreader darkreader--user-agent" media="screen">@layer {
html {
    background-color: #353533 !important;
}
html {
    color-scheme: dark !important;
}
iframe {
    color-scheme: dark !important;
}
html, body {
    background-color: #353533;
}
html, body {
    border-color: #7b7467;
    color: #d8d3c9;
}
a {
    color: #568fd0;
}
table {
    border-color: #656765;
}
mark {
    color: #d8d3c9;
}
::placeholder {
    color: #ada598;
}
input:-webkit-autofill,
textarea:-webkit-autofill,
select:-webkit-autofill {
    background-color: #535426 !important;
    color: #d8d3c9 !important;
}
* {
    scrollbar-color: #595a58 #3b3c3a;
}
::selection {
    background-color: #2c5b93 !important;
    color: #d8d3c9 !important;
}
::-moz-selection {
    background-color: #2c5b93 !important;
    color: #d8d3c9 !important;
}
}</style><meta name="referrer" content="origin"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="news.css?nHQG7fnFlccRpcf4QSYD"><style class="darkreader darkreader--sync" media="screen"></style>
        <link rel="icon" href="y18.svg">
                  <link rel="alternate" type="application/rss+xml" title="RSS" href="rss">
        <title>Hacker News</title><meta name="darkreader" content="1d3ce21066a74323ab93d39a749d141e"><style class="darkreader darkreader--override" media="screen">.vimvixen-hint {
    background-color: #6f5b27 !important;
    border-color: #98812c !important;
    color: #cbc5ba !important;
}
#vimvixen-console-frame {
    color-scheme: light !important;
}
::placeholder {
    opacity: 0.5 !important;
}
#edge-translate-panel-body,
.MuiTypography-body1,
.nfe-quote-text {
    color: var(--darkreader-neutral-text) !important;
}
gr-main-header {
    background-color: #3c585e !important;
}
.tou-z65h9k,
.tou-mignzq,
.tou-1b6i2ox,
.tou-lnqlqk {
    background-color: var(--darkreader-neutral-background) !important;
}
.tou-75mvi {
    background-color: #324c52 !important;
}
.tou-ta9e87,
.tou-1w3fhi0,
.tou-1b8t2us,
.tou-py7lfi,
.tou-1lpmd9d,
.tou-1frrtv8,
.tou-17ezmgn {
    background-color: #393a38 !important;
}
.tou-uknfeu {
    background-color: #53432a !important;
}
.tou-6i3zyv {
    background-color: #45676f !important;
}
div.mermaid-viewer-control-panel .btn {
    background-color: var(--darkreader-neutral-background);
    fill: var(--darkreader-neutral-text);
}
svg g rect.er {
    fill: var(--darkreader-neutral-background) !important;
}
svg g rect.er.entityBox {
    fill: var(--darkreader-neutral-background) !important;
}
svg g rect.er.attributeBoxOdd {
    fill: var(--darkreader-neutral-background) !important;
}
svg g rect.er.attributeBoxEven {
    fill: var(--darkreader-selection-background);
    fill-opacity: 0.8 !important;
}
svg rect.er.relationshipLabelBox {
    fill: var(--darkreader-neutral-background) !important;
}
svg g g.nodes rect,
svg g g.nodes polygon {
    fill: var(--darkreader-neutral-background) !important;
}
svg g rect.task {
    fill: var(--darkreader-selection-background) !important;
}
svg line.messageLine0,
svg line.messageLine1 {
    stroke: var(--darkreader-neutral-text) !important;
}
div.mermaid .actor {
    fill: var(--darkreader-neutral-background) !important;
}
mitid-authenticators-code-app > .code-app-container {
    background-color: white !important;
    padding-top: 1rem;
}
iframe#unpaywall[src$="unpaywall.html"] {
    color-scheme: light !important;
}
embed[type="application/pdf"][src="about:blank"] { filter: invert(100%) contrast(90%); }
#hnmain {
    background-color: var(--darkreader-neutral-background) !important;
}</style></head><body><center><table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef" data-darkreader-inline-bgcolor="" style="--darkreader-inline-bgcolor: #3b392e;">
        <tbody><tr><td bgcolor="#ff6600" data-darkreader-inline-bgcolor="" style="--darkreader-inline-bgcolor: #b4632b;"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px"><tbody><tr><td style="width:18px;padding-right:4px"><a href="https://news.ycombinator.com"><img src="y18.svg" width="18" height="18" style="border: 1px solid white; display: block; --darkreader-inline-border-top: #484947; --darkreader-inline-border-right: #484947; --darkreader-inline-border-bottom: #484947; --darkreader-inline-border-left: #484947;" data-darkreader-inline-border-top="" data-darkreader-inline-border-right="" data-darkreader-inline-border-bottom="" data-darkreader-inline-border-left=""></a></td>
                  <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a href="news">Hacker News</a></b>
                            <a href="newest">new</a> | <a href="front">past</a> | <a href="newcomments">comments</a> | <a href="ask">ask</a> | <a href="show">show</a> | <a href="jobs">jobs</a> | <a href="submit" rel="nofollow">submit</a>            </span></td><td style="text-align:right;padding-right:4px;"><span class="pagetop">
                              <a href="login?goto=news">login</a>
                          </span></td>
              </tr></tbody></table></td></tr>
<tr id="pagespace" title="" style="height:10px"></tr><tr><td><table border="0" cellpadding="0" cellspacing="0">
            <tbody><tr class="athing submission" id="42809268">
      <td align="right" valign="top" class="title"><span class="rank">1.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42809268" href="vote?id=42809268&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://mstdn.social/@isziaui/113874436953157913">A QR code that sends you to a different destination – lenticular and adversarial</a><span class="sitebit comhead"> (<a href="from?site=mstdn.social"><span class="sitestr">mstdn.social</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42809268">370 points</span> by <a href="user?id=zdw" class="hnuser">zdw</a> <span class="age" title="2025-01-23T23:55:34 1737676534"><a href="item?id=42809268">9 hours ago</a></span> <span id="unv_42809268"></span> | <a href="hide?id=42809268&amp;goto=news">hide</a> | <a href="item?id=42809268">46&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42806247">
      <td align="right" valign="top" class="title"><span class="rank">2.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42806247" href="vote?id=42806247&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="item?id=42806247">Thank HN: My bootstrapped startup got acquired today</a></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42806247">1660 points</span> by <a href="user?id=paraschopra" class="hnuser">paraschopra</a> <span class="age" title="2025-01-23T17:58:05 1737655085"><a href="item?id=42806247">15 hours ago</a></span> <span id="unv_42806247"></span> | <a href="hide?id=42806247&amp;goto=news">hide</a> | <a href="item?id=42806247">298&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42810176">
      <td align="right" valign="top" class="title"><span class="rank">3.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42810176" href="vote?id=42810176&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://lwn.net/Articles/1002342/">The State of Vim</a><span class="sitebit comhead"> (<a href="from?site=lwn.net"><span class="sitestr">lwn.net</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42810176">122 points</span> by <a href="user?id=signa11" class="hnuser">signa11</a> <span class="age" title="2025-01-24T03:22:50 1737688970"><a href="item?id=42810176">5 hours ago</a></span> <span id="unv_42810176"></span> | <a href="hide?id=42810176&amp;goto=news">hide</a> | <a href="item?id=42810176">52&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42790820">
      <td align="right" valign="top" class="title"><span class="rank">4.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42790820" href="vote?id=42790820&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree">Coping with dumb LLMs using classic ML</a><span class="sitebit comhead"> (<a href="from?site=softwaredoug.com"><span class="sitestr">softwaredoug.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42790820">22 points</span> by <a href="user?id=fzliu" class="hnuser">fzliu</a> <span class="age" title="2025-01-22T09:25:07 1737537907"><a href="item?id=42790820">2 hours ago</a></span> <span id="unv_42790820"></span> | <a href="hide?id=42790820&amp;goto=news">hide</a> | <a href="item?id=42790820">discuss</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42797260">
      <td align="right" valign="top" class="title"><span class="rank">5.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42797260" href="vote?id=42797260&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://www.byran.ee/posts/creation/">Show HN: I made an open-source laptop from scratch</a><span class="sitebit comhead"> (<a href="from?site=byran.ee"><span class="sitestr">byran.ee</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42797260">2807 points</span> by <a href="user?id=Hello9999901" class="hnuser">Hello9999901</a> <span class="age" title="2025-01-22T20:41:52 1737578512"><a href="item?id=42797260">1 day ago</a></span> <span id="unv_42797260"></span> | <a href="hide?id=42797260&amp;goto=news">hide</a> | <a href="item?id=42797260">308&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42810300">
      <td align="right" valign="top" class="title"><span class="rank">6.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42810300" href="vote?id=42810300&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://lcamtuf.substack.com/p/ui-is-hell-four-function-calculators">UI is hell: four-function calculators</a><span class="sitebit comhead"> (<a href="from?site=lcamtuf.substack.com"><span class="sitestr">lcamtuf.substack.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42810300">104 points</span> by <a href="user?id=surprisetalk" class="hnuser">surprisetalk</a> <span class="age" title="2025-01-24T03:46:19 1737690379"><a href="item?id=42810300">5 hours ago</a></span> <span id="unv_42810300"></span> | <a href="hide?id=42810300&amp;goto=news">hide</a> | <a href="item?id=42810300">39&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42810103">
      <td align="right" valign="top" class="title"><span class="rank">7.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42810103" href="vote?id=42810103&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://www.quantamagazine.org/the-jagged-monstrous-function-that-broke-calculus-20250123/">Weierstrass's Monster</a><span class="sitebit comhead"> (<a href="from?site=quantamagazine.org"><span class="sitestr">quantamagazine.org</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42810103">84 points</span> by <a href="user?id=pseudolus" class="hnuser">pseudolus</a> <span class="age" title="2025-01-24T03:02:10 1737687730"><a href="item?id=42810103">6 hours ago</a></span> <span id="unv_42810103"></span> | <a href="hide?id=42810103&amp;goto=news">hide</a> | <a href="item?id=42810103">35&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42777948">
      <td align="right" valign="top" class="title"><span class="rank">8.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42777948" href="vote?id=42777948&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://lmnt.me/blog/the-most-mario-colors.html">The Most Mario Colors</a><span class="sitebit comhead"> (<a href="from?site=lmnt.me"><span class="sitestr">lmnt.me</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42777948">402 points</span> by <a href="user?id=ingve" class="hnuser">ingve</a> <span class="age" title="2025-01-21T09:10:13 1737450613"><a href="item?id=42777948">14 hours ago</a></span> <span id="unv_42777948"></span> | <a href="hide?id=42777948&amp;goto=news">hide</a> | <a href="item?id=42777948">52&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42790902">
      <td align="right" valign="top" class="title"><span class="rank">9.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42790902" href="vote?id=42790902&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://bart.degoe.de/building-a-full-text-search-engine-150-lines-of-code/">Building a full-text search engine in 150 lines of Python code (2021)</a><span class="sitebit comhead"> (<a href="from?site=degoe.de"><span class="sitestr">degoe.de</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42790902">31 points</span> by <a href="user?id=matt_daemon" class="hnuser">matt_daemon</a> <span class="age" title="2025-01-22T09:34:50 1737538490"><a href="item?id=42790902">4 hours ago</a></span> <span id="unv_42790902"></span> | <a href="hide?id=42790902&amp;goto=news">hide</a> | <a href="item?id=42790902">9&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42806328">
      <td align="right" valign="top" class="title"><span class="rank">10.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42806328" href="vote?id=42806328&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://github.com/ggml-org/llama.vim">Llama.vim – Local LLM-assisted text completion</a><span class="sitebit comhead"> (<a href="from?site=github.com/ggml-org"><span class="sitestr">github.com/ggml-org</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42806328">417 points</span> by <a href="user?id=kgwgk" class="hnuser">kgwgk</a> <span class="age" title="2025-01-23T18:06:42 1737655602"><a href="item?id=42806328">15 hours ago</a></span> <span id="unv_42806328"></span> | <a href="hide?id=42806328&amp;goto=news">hide</a> | <a href="item?id=42806328">86&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42791036">
      <td align="right" valign="top" class="title"><span class="rank">11.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42791036" href="vote?id=42791036&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://mukulrathi.com/create-your-own-programming-language/intro-to-compiler/">I wrote my own "proper" programming language (2020)</a><span class="sitebit comhead"> (<a href="from?site=mukulrathi.com"><span class="sitestr">mukulrathi.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42791036">18 points</span> by <a href="user?id=upmind" class="hnuser">upmind</a> <span class="age" title="2025-01-22T09:54:25 1737539665"><a href="item?id=42791036">3 hours ago</a></span> <span id="unv_42791036"></span> | <a href="hide?id=42791036&amp;goto=news">hide</a> | <a href="item?id=42791036">4&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42806301">
      <td align="right" valign="top" class="title"><span class="rank">12.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42806301" href="vote?id=42806301&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://openai.com/index/introducing-operator/">Operator research preview</a><span class="sitebit comhead"> (<a href="from?site=openai.com"><span class="sitestr">openai.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42806301">366 points</span> by <a href="user?id=meetpateltech" class="hnuser">meetpateltech</a> <span class="age" title="2025-01-23T18:03:40 1737655420"><a href="item?id=42806301">15 hours ago</a></span> <span id="unv_42806301"></span> | <a href="hide?id=42806301&amp;goto=news">hide</a> | <a href="item?id=42806301">321&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42780490">
      <td align="right" valign="top" class="title"><span class="rank">13.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42780490" href="vote?id=42780490&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://spectrum.ieee.org/reconnaissance-satellite" rel="nofollow">A Cold War Satellite Program Called Parcae Revolutionized Signals Intelligence</a><span class="sitebit comhead"> (<a href="from?site=ieee.org"><span class="sitestr">ieee.org</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42780490">5 points</span> by <a href="user?id=kungfudoi" class="hnuser">kungfudoi</a> <span class="age" title="2025-01-21T14:33:29 1737470009"><a href="item?id=42780490">1 hour ago</a></span> <span id="unv_42780490"></span> | <a href="hide?id=42780490&amp;goto=news">hide</a> | <a href="item?id=42780490">discuss</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42808801">
      <td align="right" valign="top" class="title"><span class="rank">14.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42808801" href="vote?id=42808801&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://jprx.io/cve-2024-54507/">Susctl CVE-2024-54507: A particularly 'sus' sysctl in the XNU kernel</a><span class="sitebit comhead"> (<a href="from?site=jprx.io"><span class="sitestr">jprx.io</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42808801">115 points</span> by <a href="user?id=jprx" class="hnuser">jprx</a> <span class="age" title="2025-01-23T22:37:57 1737671877"><a href="item?id=42808801">10 hours ago</a></span> <span id="unv_42808801"></span> | <a href="hide?id=42808801&amp;goto=news">hide</a> | <a href="item?id=42808801">31&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42811332">
      <td align="right" valign="top" class="title"><span class="rank">15.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42811332" href="vote?id=42811332&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://www.thebookseller.com/news/amazon-uk-to-stop-selling-bloomsburys-books">Amazon UK to stop selling Bloomsbury's books</a><span class="sitebit comhead"> (<a href="from?site=thebookseller.com"><span class="sitestr">thebookseller.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42811332">19 points</span> by <a href="user?id=nickcotter" class="hnuser">nickcotter</a> <span class="age" title="2025-01-24T07:55:01 1737705301"><a href="item?id=42811332">1 hour ago</a></span> <span id="unv_42811332"></span> | <a href="hide?id=42811332&amp;goto=news">hide</a> | <a href="item?id=42811332">7&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42806486">
      <td align="right" valign="top" class="title"><span class="rank">16.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42806486" href="vote?id=42806486&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://www.guedelon.fr/en/">Building a Medieval Castle from Scratch</a><span class="sitebit comhead"> (<a href="from?site=guedelon.fr"><span class="sitestr">guedelon.fr</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42806486">225 points</span> by <a href="user?id=CharlesW" class="hnuser">CharlesW</a> <span class="age" title="2025-01-23T18:24:30 1737656670"><a href="item?id=42806486">14 hours ago</a></span> <span id="unv_42806486"></span> | <a href="hide?id=42806486&amp;goto=news">hide</a> | <a href="item?id=42806486">75&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42791465">
      <td align="right" valign="top" class="title"><span class="rank">17.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42791465" href="vote?id=42791465&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="http://0x80.pl/notesen/2025-01-21-loongarch64-highlights.html">LoongArch64 Subjective Higlights</a><span class="sitebit comhead"> (<a href="from?site=0x80.pl"><span class="sitestr">0x80.pl</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42791465">27 points</span> by <a href="user?id=camel-cdr" class="hnuser">camel-cdr</a> <span class="age" title="2025-01-22T11:07:45 1737544065"><a href="item?id=42791465">5 hours ago</a></span> <span id="unv_42791465"></span> | <a href="hide?id=42791465&amp;goto=news">hide</a> | <a href="item?id=42791465">4&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42808889">
      <td align="right" valign="top" class="title"><span class="rank">18.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42808889" href="vote?id=42808889&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://github.com/runevision/Dither3D">Surface-Stable Fractal Dithering</a><span class="sitebit comhead"> (<a href="from?site=github.com/runevision"><span class="sitestr">github.com/runevision</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42808889">122 points</span> by <a href="user?id=bj-rn" class="hnuser">bj-rn</a> <span class="age" title="2025-01-23T22:50:11 1737672611"><a href="item?id=42808889">10 hours ago</a></span> <span id="unv_42808889"></span> | <a href="hide?id=42808889&amp;goto=news">hide</a> | <a href="item?id=42808889">16&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42809034">
      <td align="right" valign="top" class="title"><span class="rank">19.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42809034" href="vote?id=42809034&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://chipsandcheese.com/p/disabling-zen-5s-op-cache-and-exploring">Disabling Zen 5's Op Cache and Exploring Its Clustered Decoder</a><span class="sitebit comhead"> (<a href="from?site=chipsandcheese.com"><span class="sitestr">chipsandcheese.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42809034">69 points</span> by <a href="user?id=mfiguiere" class="hnuser">mfiguiere</a> <span class="age" title="2025-01-23T23:14:46 1737674086"><a href="item?id=42809034">10 hours ago</a></span> <span id="unv_42809034"></span> | <a href="hide?id=42809034&amp;goto=news">hide</a> | <a href="item?id=42809034">1&nbsp;comment</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42804566">
      <td align="right" valign="top" class="title"><span class="rank">20.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42804566" href="vote?id=42804566&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://benpence.com/blog/post/psychedelic-graphics-0">Psychedelic Graphics 0: Introduction</a><span class="sitebit comhead"> (<a href="from?site=benpence.com"><span class="sitestr">benpence.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42804566">257 points</span> by <a href="user?id=mwfogleman" class="hnuser">mwfogleman</a> <span class="age" title="2025-01-23T14:49:43 1737643783"><a href="item?id=42804566">17 hours ago</a></span> <span id="unv_42804566"></span> | <a href="hide?id=42804566&amp;goto=news">hide</a> | <a href="item?id=42804566">59&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42803279">
      <td align="right" valign="top" class="title"><span class="rank">21.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42803279" href="vote?id=42803279&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://samcurry.net/hacking-subaru">Hacking Subaru: Tracking and controlling cars via the admin panel</a><span class="sitebit comhead"> (<a href="from?site=samcurry.net"><span class="sitestr">samcurry.net</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42803279">416 points</span> by <a href="user?id=ramimac" class="hnuser">ramimac</a> <span class="age" title="2025-01-23T12:22:19 1737634939"><a href="item?id=42803279">20 hours ago</a></span> <span id="unv_42803279"></span> | <a href="hide?id=42803279&amp;goto=news">hide</a> | <a href="item?id=42803279">249&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42806616">
      <td align="right" valign="top" class="title"><span class="rank">22.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42806616" href="vote?id=42806616&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://github.com/fal-ai-community/video-starter-kit">Show HN: Open-source AI video editor</a><span class="sitebit comhead"> (<a href="from?site=github.com/fal-ai-community"><span class="sitestr">github.com/fal-ai-community</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42806616">204 points</span> by <a href="user?id=drochetti" class="hnuser">drochetti</a> <span class="age" title="2025-01-23T18:34:38 1737657278"><a href="item?id=42806616">14 hours ago</a></span> <span id="unv_42806616"></span> | <a href="hide?id=42806616&amp;goto=news">hide</a> | <a href="item?id=42806616">33&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42809578">
      <td align="right" valign="top" class="title"><span class="rank">23.</span></td>      <td><img src="s.gif" height="1" width="14"></td>       <td class="title"><span class="titleline"><a href="https://www.ycombinator.com/companies/sei/jobs/LeAtLYf-full-stack-engineer-typescript-react-gen-ai">Sei (YC W22) Is Hiring</a><span class="sitebit comhead"> (<a href="from?site=ycombinator.com"><span class="sitestr">ycombinator.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="age" title="2025-01-24T01:00:52 1737680452"><a href="item?id=42809578">8 hours ago</a></span> | <a href="hide?id=42809578&amp;goto=news">hide</a>      </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42809990">
      <td align="right" valign="top" class="title"><span class="rank">24.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42809990" href="vote?id=42809990&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://blog.vectorchord.ai/supercharge-vector-search-with-colbert-rerank-in-postgresql">Supercharge vector search with ColBERT rerank in PostgreSQL</a><span class="sitebit comhead"> (<a href="from?site=vectorchord.ai"><span class="sitestr">vectorchord.ai</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42809990">29 points</span> by <a href="user?id=gaocegege" class="hnuser">gaocegege</a> <span class="age" title="2025-01-24T02:28:10 1737685690"><a href="item?id=42809990">6 hours ago</a></span> <span id="unv_42809990"></span> | <a href="hide?id=42809990&amp;goto=news">hide</a> | <a href="item?id=42809990">8&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42800893">
      <td align="right" valign="top" class="title"><span class="rank">25.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42800893" href="vote?id=42800893&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://t4t.social/">Show HN: I built an active community of trans people online</a><span class="sitebit comhead"> (<a href="from?site=t4t.social"><span class="sitestr">t4t.social</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42800893">405 points</span> by <a href="user?id=t4t" class="hnuser">t4t</a> <span class="age" title="2025-01-23T05:07:35 1737608855"><a href="item?id=42800893">16 hours ago</a></span> <span id="unv_42800893"></span> | <a href="hide?id=42800893&amp;goto=news">hide</a> | <a href="item?id=42800893">243&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42805425">
      <td align="right" valign="top" class="title"><span class="rank">26.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42805425" href="vote?id=42805425&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://danluu.com/deconstruct-files/">Working with Files Is Hard (2019)</a><span class="sitebit comhead"> (<a href="from?site=danluu.com"><span class="sitestr">danluu.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42805425">169 points</span> by <a href="user?id=nathan_phoenix" class="hnuser">nathan_phoenix</a> <span class="age" title="2025-01-23T16:28:34 1737649714"><a href="item?id=42805425">16 hours ago</a></span> <span id="unv_42805425"></span> | <a href="hide?id=42805425&amp;goto=news">hide</a> | <a href="item?id=42805425">79&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42804835">
      <td align="right" valign="top" class="title"><span class="rank">27.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42804835" href="vote?id=42804835&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://github.com/yassinebenaid/bunster">Bunster: Compile bash scripts to self contained executables</a><span class="sitebit comhead"> (<a href="from?site=github.com/yassinebenaid"><span class="sitestr">github.com/yassinebenaid</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42804835">180 points</span> by <a href="user?id=thunderbong" class="hnuser">thunderbong</a> <span class="age" title="2025-01-23T15:17:26 1737645446"><a href="item?id=42804835">17 hours ago</a></span> <span id="unv_42804835"></span> | <a href="hide?id=42804835&amp;goto=news">hide</a> | <a href="item?id=42804835">71&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42775422">
      <td align="right" valign="top" class="title"><span class="rank">28.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42775422" href="vote?id=42775422&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://www.doc.ic.ac.uk/~afd/papers/2025/ICST-Industry.pdf">Compiler Fuzzing in Continuous Integration: A Case Study on Dafny [pdf]</a><span class="sitebit comhead"> (<a href="from?site=ic.ac.uk"><span class="sitestr">ic.ac.uk</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42775422">31 points</span> by <a href="user?id=matt_d" class="hnuser">matt_d</a> <span class="age" title="2025-01-21T01:38:57 1737423537"><a href="item?id=42775422">8 hours ago</a></span> <span id="unv_42775422"></span> | <a href="hide?id=42775422&amp;goto=news">hide</a> | <a href="item?id=42775422">1&nbsp;comment</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42789372">
      <td align="right" valign="top" class="title"><span class="rank">29.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42789372" href="vote?id=42789372&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://ivanbelenky.com/articles/capacitors">Capacitors Meet Geometric Series</a><span class="sitebit comhead"> (<a href="from?site=ivanbelenky.com"><span class="sitestr">ivanbelenky.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42789372">27 points</span> by <a href="user?id=ivanbelenky" class="hnuser">ivanbelenky</a> <span class="age" title="2025-01-22T05:34:15 1737524055"><a href="item?id=42789372">9 hours ago</a></span> <span id="unv_42789372"></span> | <a href="hide?id=42789372&amp;goto=news">hide</a> | <a href="item?id=42789372">discuss</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing submission" id="42804434">
      <td align="right" valign="top" class="title"><span class="rank">30.</span></td>      <td valign="top" class="votelinks"><center><a id="up_42804434" href="vote?id=42804434&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://dhruvvidyut.co.in/">Turn any bicycle electric</a><span class="sitebit comhead"> (<a href="from?site=dhruvvidyut.co.in"><span class="sitestr">dhruvvidyut.co.in</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_42804434">293 points</span> by <a href="user?id=samdung" class="hnuser">samdung</a> <span class="age" title="2025-01-23T14:38:09 1737643089"><a href="item?id=42804434">18 hours ago</a></span> <span id="unv_42804434"></span> | <a href="hide?id=42804434&amp;goto=news">hide</a> | <a href="item?id=42804434">163&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
            <tr class="morespace" style="height:10px"></tr><tr><td colspan="2"></td>
      <td class="title"><a href="?p=2" class="morelink" rel="next">More</a></td>    </tr>
  </tbody></table>
</td></tr>
<tr><td><img src="s.gif" height="10" width="0"><table width="100%" cellspacing="0" cellpadding="1"><tbody><tr><td bgcolor="#ff6600" data-darkreader-inline-bgcolor="" style="--darkreader-inline-bgcolor: #b4632b;"></td></tr></tbody></table><br>
<center><a href="https://www.ycombinator.com/apply/">Consider applying for YC's Spring batch! Applications are open till Feb 11.</a></center><br>
<center><span class="yclinks"><a href="newsguidelines.html">Guidelines</a> | <a href="newsfaq.html">FAQ</a> | <a href="lists">Lists</a> | <a href="https://github.com/HackerNews/API">API</a> | <a href="security.html">Security</a> | <a href="https://www.ycombinator.com/legal/">Legal</a> | <a href="https://www.ycombinator.com/apply/">Apply to YC</a> | <a href="mailto:hn@ycombinator.com">Contact</a></span><br><br>
<form method="get" action="//hn.algolia.com/">Search: <input type="text" name="q" size="17" autocorrect="off" spellcheck="false" autocapitalize="off" autocomplete="off"></form></center></td></tr>      </tbody></table></center>
      <script type="text/javascript" src="hn.js?nHQG7fnFlccRpcf4QSYD"></script>
  
</body></html>"""


parser = bs4.BeautifulSoup(html, features="lxml")
hackerNewsUrls = seq(parser.select("tr > td.subtext > span.subline > span.age > a")).map(lambda x: "https://news.ycombinator.com/" + x['href']).to_list()
titles = seq(parser.select(".titleline > a")).map(lambda x: x.text).to_list()
urls = seq(parser.select(".titleline > a")).map(lambda x: x['href']).map(lambda x: "https://news.ycombinator.com/" + x if x.startswith("item?id") else x).to_list()

dates = seq(parser.select("tr > td.subtext > span.subline > span.age")).map(lambda x: x['title']).map(lambda x: datetime.fromtimestamp(int(re.findall(r"[0-9]{10,}", x)[0]), timezone.utc)).to_list()

print(dates)
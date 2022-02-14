import panel as pn
import numpy as np
import holoviews as hv


import param
from panel.template.theme import Theme


'https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/style.css'
'<link rel="stylesheet" href="https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/style.css">'

template = '''
{% extends base %}

<!-- goes in head -->
{% block postamble %}
<style>img.lazy{min-height:1px}</style><link
rel=preload href=https://cioosatlantic.ca/wp-content/plugins/w3-total-cache/pub/js/lazyload.min.js?x48800 as=script><meta
charset="UTF-8"><meta
name="viewport" content="width=device-width, initial-scale=1"><meta
name="description" content="The Canadian Integrated Ocean Observing System (CIOOS) is a powerful open-access platform for sharing information about the state of our oceans."><link
rel=profile href=https://gmpg.org/xfn/11><link
rel=pingback href=https://cioosatlantic.ca/xmlrpc.php><link
rel=preconnect href=https://fonts.googleapis.com crossorigin><link
rel=preconnect href=https://fonts.gstatic.com crossorigin><title>Data Tools &#8211; CIOOS Atlantic</title><meta
name='robots' content='max-image-preview:large'><link
rel=alternate href=https://cioosatlantic.ca/data-tools/ hreflang=en><link
rel=alternate href=https://cioosatlantic.ca/fr/outils/ hreflang=fr><link
rel=alternate type=application/rss+xml title="CIOOS Atlantic &raquo; Feed" href=https://cioosatlantic.ca/feed/ ><link
rel=alternate type=application/rss+xml title="CIOOS Atlantic &raquo; Comments Feed" href=https://cioosatlantic.ca/comments/feed/ ><link
rel=stylesheet href=https://cioosatlantic.ca/wp-content/cache/minify/a5ff7.css?x48800 media=all><style id=global-styles-inline-css>/*<![CDATA[*/body{--wp--preset--color--black: #000000;--wp--preset--color--cyan-bluish-gray: #abb8c3;--wp--preset--color--white: #ffffff;--wp--preset--color--pale-pink: #f78da7;--wp--preset--color--vivid-red: #cf2e2e;--wp--preset--color--luminous-vivid-orange: #ff6900;--wp--preset--color--luminous-vivid-amber: #fcb900;--wp--preset--color--light-green-cyan: #7bdcb5;--wp--preset--color--vivid-green-cyan: #00d084;--wp--preset--color--pale-cyan-blue: #8ed1fc;--wp--preset--color--vivid-cyan-blue: #0693e3;--wp--preset--color--vivid-purple: #9b51e0;--wp--preset--gradient--vivid-cyan-blue-to-vivid-purple: linear-gradient(135deg,rgba(6,147,227,1) 0%,rgb(155,81,224) 100%);--wp--preset--gradient--light-green-cyan-to-vivid-green-cyan: linear-gradient(135deg,rgb(122,220,180) 0%,rgb(0,208,130) 100%);--wp--preset--gradient--luminous-vivid-amber-to-luminous-vivid-orange: linear-gradient(135deg,rgba(252,185,0,1) 0%,rgba(255,105,0,1) 100%);--wp--preset--gradient--luminous-vivid-orange-to-vivid-red: linear-gradient(135deg,rgba(255,105,0,1) 0%,rgb(207,46,46) 100%);--wp--preset--gradient--very-light-gray-to-cyan-bluish-gray: linear-gradient(135deg,rgb(238,238,238) 0%,rgb(169,184,195) 100%);--wp--preset--gradient--cool-to-warm-spectrum: linear-gradient(135deg,rgb(74,234,220) 0%,rgb(151,120,209) 20%,rgb(207,42,186) 40%,rgb(238,44,130) 60%,rgb(251,105,98) 80%,rgb(254,248,76) 100%);--wp--preset--gradient--blush-light-purple: linear-gradient(135deg,rgb(255,206,236) 0%,rgb(152,150,240) 100%);--wp--preset--gradient--blush-bordeaux: linear-gradient(135deg,rgb(254,205,165) 0%,rgb(254,45,45) 50%,rgb(107,0,62) 100%);--wp--preset--gradient--luminous-dusk: linear-gradient(135deg,rgb(255,203,112) 0%,rgb(199,81,192) 50%,rgb(65,88,208) 100%);--wp--preset--gradient--pale-ocean: linear-gradient(135deg,rgb(255,245,203) 0%,rgb(182,227,212) 50%,rgb(51,167,181) 100%);--wp--preset--gradient--electric-grass: linear-gradient(135deg,rgb(202,248,128) 0%,rgb(113,206,126) 100%);--wp--preset--gradient--midnight: linear-gradient(135deg,rgb(2,3,129) 0%,rgb(40,116,252) 100%);--wp--preset--duotone--dark-grayscale: url('#wp-duotone-dark-grayscale');--wp--preset--duotone--grayscale: url('#wp-duotone-grayscale');--wp--preset--duotone--purple-yellow: url('#wp-duotone-purple-yellow');--wp--preset--duotone--blue-red: url('#wp-duotone-blue-red');--wp--preset--duotone--midnight: url('#wp-duotone-midnight');--wp--preset--duotone--magenta-yellow: url('#wp-duotone-magenta-yellow');--wp--preset--duotone--purple-green: url('#wp-duotone-purple-green');--wp--preset--duotone--blue-orange: url('#wp-duotone-blue-orange');--wp--preset--font-size--small: 13px;--wp--preset--font-size--medium: 20px;--wp--preset--font-size--large: 36px;--wp--preset--font-size--x-large: 42px;}.has-black-color{color: var(--wp--preset--color--black) !important;}.has-cyan-bluish-gray-color{color: var(--wp--preset--color--cyan-bluish-gray) !important;}.has-white-color{color: var(--wp--preset--color--white) !important;}.has-pale-pink-color{color: var(--wp--preset--color--pale-pink) !important;}.has-vivid-red-color{color: var(--wp--preset--color--vivid-red) !important;}.has-luminous-vivid-orange-color{color: var(--wp--preset--color--luminous-vivid-orange) !important;}.has-luminous-vivid-amber-color{color: var(--wp--preset--color--luminous-vivid-amber) !important;}.has-light-green-cyan-color{color: var(--wp--preset--color--light-green-cyan) !important;}.has-vivid-green-cyan-color{color: var(--wp--preset--color--vivid-green-cyan) !important;}.has-pale-cyan-blue-color{color: var(--wp--preset--color--pale-cyan-blue) !important;}.has-vivid-cyan-blue-color{color: var(--wp--preset--color--vivid-cyan-blue) !important;}.has-vivid-purple-color{color: var(--wp--preset--color--vivid-purple) !important;}.has-black-background-color{background-color: var(--wp--preset--color--black) !important;}.has-cyan-bluish-gray-background-color{background-color: var(--wp--preset--color--cyan-bluish-gray) !important;}.has-white-background-color{background-color: var(--wp--preset--color--white) !important;}.has-pale-pink-background-color{background-color: var(--wp--preset--color--pale-pink) !important;}.has-vivid-red-background-color{background-color: var(--wp--preset--color--vivid-red) !important;}.has-luminous-vivid-orange-background-color{background-color: var(--wp--preset--color--luminous-vivid-orange) !important;}.has-luminous-vivid-amber-background-color{background-color: var(--wp--preset--color--luminous-vivid-amber) !important;}.has-light-green-cyan-background-color{background-color: var(--wp--preset--color--light-green-cyan) !important;}.has-vivid-green-cyan-background-color{background-color: var(--wp--preset--color--vivid-green-cyan) !important;}.has-pale-cyan-blue-background-color{background-color: var(--wp--preset--color--pale-cyan-blue) !important;}.has-vivid-cyan-blue-background-color{background-color: var(--wp--preset--color--vivid-cyan-blue) !important;}.has-vivid-purple-background-color{background-color: var(--wp--preset--color--vivid-purple) !important;}.has-black-border-color{border-color: var(--wp--preset--color--black) !important;}.has-cyan-bluish-gray-border-color{border-color: var(--wp--preset--color--cyan-bluish-gray) !important;}.has-white-border-color{border-color: var(--wp--preset--color--white) !important;}.has-pale-pink-border-color{border-color: var(--wp--preset--color--pale-pink) !important;}.has-vivid-red-border-color{border-color: var(--wp--preset--color--vivid-red) !important;}.has-luminous-vivid-orange-border-color{border-color: var(--wp--preset--color--luminous-vivid-orange) !important;}.has-luminous-vivid-amber-border-color{border-color: var(--wp--preset--color--luminous-vivid-amber) !important;}.has-light-green-cyan-border-color{border-color: var(--wp--preset--color--light-green-cyan) !important;}.has-vivid-green-cyan-border-color{border-color: var(--wp--preset--color--vivid-green-cyan) !important;}.has-pale-cyan-blue-border-color{border-color: var(--wp--preset--color--pale-cyan-blue) !important;}.has-vivid-cyan-blue-border-color{border-color: var(--wp--preset--color--vivid-cyan-blue) !important;}.has-vivid-purple-border-color{border-color: var(--wp--preset--color--vivid-purple) !important;}.has-vivid-cyan-blue-to-vivid-purple-gradient-background{background: var(--wp--preset--gradient--vivid-cyan-blue-to-vivid-purple) !important;}.has-light-green-cyan-to-vivid-green-cyan-gradient-background{background: var(--wp--preset--gradient--light-green-cyan-to-vivid-green-cyan) !important;}.has-luminous-vivid-amber-to-luminous-vivid-orange-gradient-background{background: var(--wp--preset--gradient--luminous-vivid-amber-to-luminous-vivid-orange) !important;}.has-luminous-vivid-orange-to-vivid-red-gradient-background{background: var(--wp--preset--gradient--luminous-vivid-orange-to-vivid-red) !important;}.has-very-light-gray-to-cyan-bluish-gray-gradient-background{background: var(--wp--preset--gradient--very-light-gray-to-cyan-bluish-gray) !important;}.has-cool-to-warm-spectrum-gradient-background{background: var(--wp--preset--gradient--cool-to-warm-spectrum) !important;}.has-blush-light-purple-gradient-background{background: var(--wp--preset--gradient--blush-light-purple) !important;}.has-blush-bordeaux-gradient-background{background: var(--wp--preset--gradient--blush-bordeaux) !important;}.has-luminous-dusk-gradient-background{background: var(--wp--preset--gradient--luminous-dusk) !important;}.has-pale-ocean-gradient-background{background: var(--wp--preset--gradient--pale-ocean) !important;}.has-electric-grass-gradient-background{background: var(--wp--preset--gradient--electric-grass) !important;}.has-midnight-gradient-background{background: var(--wp--preset--gradient--midnight) !important;}.has-small-font-size{font-size: var(--wp--preset--font-size--small) !important;}.has-medium-font-size{font-size: var(--wp--preset--font-size--medium) !important;}.has-large-font-size{font-size: var(--wp--preset--font-size--large) !important;}.has-x-large-font-size{font-size: var(--wp--preset--font-size--x-large) !important;}/*]]>*/</style><link
rel=stylesheet href=https://cioosatlantic.ca/wp-content/cache/minify/454a6.css?x48800 media=all><link
rel=stylesheet href=https://cioosatlantic.ca/wp-content/cache/minify/2210e.css?x48800 media=all><link
rel=stylesheet href=https://cioosatlantic.ca/wp-content/cache/minify/300ec.css?x48800 media=all><script src=https://cioosatlantic.ca/wp-content/cache/minify/d52ed.js?x48800></script> <script src=https://cioosatlantic.ca/wp-content/cache/minify/63b1f.js?x48800></script> <script src=https://cioosatlantic.ca/wp-content/cache/minify/6c459.js?x48800></script> <script src=https://cioosatlantic.ca/wp-content/cache/minify/f8aab.js?x48800></script> <link
rel=https://api.w.org/ href=https://cioosatlantic.ca/wp-json/ ><link
rel=alternate type=application/json href=https://cioosatlantic.ca/wp-json/wp/v2/pages/2787><link
rel=EditURI type=application/rsd+xml title=RSD href=https://cioosatlantic.ca/xmlrpc.php?rsd><link
rel=wlwmanifest type=application/wlwmanifest+xml href=https://cioosatlantic.ca/wp-includes/wlwmanifest.xml><meta
name="generator" content="WordPress 5.9"><link
rel=canonical href=https://cioosatlantic.ca/data-tools/ ><link
rel=shortlink href='https://cioosatlantic.ca/?p=2787'><link
rel=alternate type=application/json+oembed href="https://cioosatlantic.ca/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fcioosatlantic.ca%2Fdata-tools%2F"><link
rel=alternate type=text/xml+oembed href="https://cioosatlantic.ca/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fcioosatlantic.ca%2Fdata-tools%2F&#038;format=xml"><style>.site-title,
			.site-description {
				position: absolute;
				clip: rect(1px, 1px, 1px, 1px);
				}</style><link
rel=icon href=https://cioosatlantic.ca/wp-content/uploads/cioos-atlantic-favicon.ico?x48800 sizes=32x32><link
rel=icon href=https://cioosatlantic.ca/wp-content/uploads/cioos-atlantic-favicon.ico?x48800 sizes=192x192><link
rel=apple-touch-icon href=https://cioosatlantic.ca/wp-content/uploads/cioos-atlantic-favicon.ico?x48800><meta
name="msapplication-TileImage" content="https://cioosatlantic.ca/wp-content/uploads/cioos-atlantic-favicon.ico"><style id=wp-custom-css>@-webkit-keyframes carousel-animate-vertical {
  0% {
    -webkit-transform: translateY(100%) scale(0.5);
    transform: translateY(100%) scale(0.5);
    opacity: 0;
    visibility: hidden; }
  3%,
  16.66667% {
    -webkit-transform: translateY(100%) scale(0.7);
    transform: translateY(100%) scale(0.7);
    opacity: .4;
    visibility: visible; }
  19.66667%,
  33.33333% {
    -webkit-transform: translateY(0) scale(1);
    transform: translateY(0) scale(1);
    opacity: 1;
    visibility: visible; }
  36.33333%,
  50% {
    -webkit-transform: translateY(-100%) scale(0.7);
    transform: translateY(-100%) scale(0.7);
    opacity: .4;
    visibility: visible; }
  53% {
    -webkit-transform: translateY(-100%) scale(0.5);
    transform: translateY(-100%) scale(0.5);
    opacity: 0;
    visibility: visible; }
  100% {
    -webkit-transform: translateY(-100%) scale(0.5);
    transform: translateY(-100%) scale(0.5);
    opacity: 0;
    visibility: hidden; } }

@keyframes carousel-animate-vertical {
  0% {
    -webkit-transform: translateY(100%) scale(0.5);
    transform: translateY(100%) scale(0.5);
    opacity: 0;
    visibility: hidden; }
  3%,
  16.66667% {
    -webkit-transform: translateY(100%) scale(0.7);
    transform: translateY(100%) scale(0.7);
    opacity: .4;
    visibility: visible; }
  19.66667%,
  33.33333% {
    -webkit-transform: translateY(0) scale(1);
    transform: translateY(0) scale(1);
    opacity: 1;
    visibility: visible; }
  36.33333%,
  50% {
    -webkit-transform: translateY(-100%) scale(0.7);
    transform: translateY(-100%) scale(0.7);
    opacity: .4;
    visibility: visible; }
  53% {
    -webkit-transform: translateY(-100%) scale(0.5);
    transform: translateY(-100%) scale(0.5);
    opacity: 0;
    visibility: visible; }
  100% {
    -webkit-transform: translateY(-100%) scale(0.5);
    transform: translateY(-100%) scale(0.5);
    opacity: 0;
    visibility: hidden; } }

@-webkit-keyframes animate-slider-two {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0); }
  100% {
    -webkit-transform: translateX(calc(-570px * 2));
    transform: translateX(calc(-570px * 2)); } }

@keyframes animate-slider-two {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0); }
  100% {
    -webkit-transform: translateX(calc(-570px * 2));
    transform: translateX(calc(-570px * 2)); } }

@-webkit-keyframes animate-slider-six {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0); }
  100% {
    -webkit-transform: translateX(calc(-225px * 6));
    transform: translateX(calc(-225px * 6)); } }

@keyframes animate-slider-six {
  0% {
    -webkit-transform: translateX(0);
    transform: translateX(0); }
  100% {
    -webkit-transform: translateX(calc(-225px * 6));
    transform: translateX(calc(-225px * 6)); } }

.slider {
  margin: auto;
  height: 100px;
  overflow: hidden;
  position: relative;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center; }
  .slider::before, .slider::after {
    background: -webkit-gradient(linear, left top, right top, from(white), to(rgba(255, 255, 255, 0)));
    background: -webkit-linear-gradient(left, white 0%, rgba(255, 255, 255, 0) 100%);
    background: -o-linear-gradient(left, white 0%, rgba(255, 255, 255, 0) 100%);
    background: linear-gradient(to right, white 0%, rgba(255, 255, 255, 0) 100%);
    content: "";
    height: 100px;
    position: absolute;
    width: 100px;
    z-index: 2; }
  .slider::after {
    right: 0;
    top: 0;
    -webkit-transform: rotateZ(180deg);
    -ms-transform: rotate(180deg);
    transform: rotateZ(180deg); }
  .slider::before {
    left: 0;
    top: 0; }
  .slider .slider-track {
    display: -ms-grid;
    display: grid;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    height: 100%; }
    .slider .slider-track .slider-item img {
      max-width: 150px;
      max-height: 50px;
      max-width: initial; }
    .slider .slider-track.slider-track__two {
      -ms-grid-columns: (1fr)[4];
      grid-template-columns: repeat(4, 1fr);
      width: calc(570px*4);
      -webkit-animation: animate-slider-two 38s linear infinite;
      animation: animate-slider-two 38s linear infinite; }
      .slider .slider-track.slider-track__two .slider-item {
        width: 570px; }
    .slider .slider-track.slider-track__six {
      -ms-grid-columns: (1fr)[12];
      grid-template-columns: repeat(12, 1fr);
      width: calc(225px*12);
      -webkit-animation: animate-slider-six 45s linear infinite;
      animation: animate-slider-six 45s linear infinite; }
      .slider .slider-track.slider-track__six .slider-item {
        width: 225px; }

@media screen and (min-width: 1300px) {
  .slider {
    width: 1140px; } }

@media screen and (min-width: 1000px) and (max-width: 1299px) {
  .slider {
    width: 800px; } }

@media screen and (min-width: 600px) and (max-width: 799px) {
  .slider {
    width: 500px; } }

@media screen and (max-width: 599px) {
  .slider {
    width: 400px; } }
.hidden {
	display: none;
}</style>
{% endblock %}

<!-- goes in body -->
{% block body %}
<body class="page-template-default page page-id-2787 atlantic no-sidebar">
<style>/*<![CDATA[*/#wpfront-notification-bar, #wpfront-notification-bar-editor            {
            background: #17212B;
            background: -moz-linear-gradient(top, #17212B 0%, #17212B 100%);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#17212B), color-stop(100%,#17212B));
            background: -webkit-linear-gradient(top, #17212B 0%,#17212B 100%);
            background: -o-linear-gradient(top, #17212B 0%,#17212B 100%);
            background: -ms-linear-gradient(top, #17212B 0%,#17212B 100%);
            background: linear-gradient(to bottom, #17212B 0%, #17212B 100%);
            filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#17212B', endColorstr='#17212B',GradientType=0 );
            background-repeat: no-repeat;
                        }
            #wpfront-notification-bar div.wpfront-message, #wpfront-notification-bar-editor li, #wpfront-notification-bar-editor p            {
            color: #ffffff;
                        }
            #wpfront-notification-bar a.wpfront-button, #wpfront-notification-bar-editor a.wpfront-button            {
            background: #00b7ea;
            background: -moz-linear-gradient(top, #00b7ea 0%, #009ec3 100%);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#00b7ea), color-stop(100%,#009ec3));
            background: -webkit-linear-gradient(top, #00b7ea 0%,#009ec3 100%);
            background: -o-linear-gradient(top, #00b7ea 0%,#009ec3 100%);
            background: -ms-linear-gradient(top, #00b7ea 0%,#009ec3 100%);
            background: linear-gradient(to bottom, #00b7ea 0%, #009ec3 100%);
            filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#00b7ea', endColorstr='#009ec3',GradientType=0 );

            color: #ffffff;
            }
            #wpfront-notification-bar-open-button            {
            background-color: #00b7ea;
            right: 10px;
                        }
            #wpfront-notification-bar-open-button.top                {
                background-image: url(https://cioosatlantic.ca/wp-content/plugins/wpfront-notification-bar/images/arrow_down.png);
                }

                #wpfront-notification-bar-open-button.bottom                {
                background-image: url(https://cioosatlantic.ca/wp-content/plugins/wpfront-notification-bar/images/arrow_up.png);
                }
                #wpfront-notification-bar-table, .wpfront-notification-bar tbody, .wpfront-notification-bar tr            {
                        }
            #wpfront-notification-bar div.wpfront-close            {
            border: 1px solid #555555;
            background-color: #555555;
            color: #000000;
            }
            #wpfront-notification-bar div.wpfront-close:hover            {
            border: 1px solid #aaaaaa;
            background-color: #aaaaaa;
            }
             #wpfront-notification-bar-spacer { display:block; }/* Site wide notification */ #wpfront-notification-bar-spacer { background-color:transparent; z-index: 100000; /*position: absolute;*/ overflow: hidden; top: 45px; } /* if logged in && admin bar */ .logged-in.admin-bar #wpfront-notification-bar-spacer { top: 77px; } /* push down header (will cause problems if lightbox is used for anything else, need specific class for alerts) */ .dialog-lightbox-body.dialog-container.dialog-lightbox-container #header { margin: 8.5em 0 3em; } #wpfront-notification-bar-spacer .elementor-section.elementor-section-boxed { padding: 0; background-color: #f4f4f4; } #wpfront-notification-bar-spacer .elementor-section #wpfront-notification-bar .elementor-element-populated { padding: 14px 0 15px; } #wpfront-notification-bar-spacer .elementor-section .elementor-element .elementor-heading-title { color: #808081; } #wpfront-notification-bar-spacer #wpfront-notification-bar { font-size: 14px; text-align: center; font-weight: 700; } #wpfront-notification-bar-spacer #wpfront-notification-bar span { display: block; color: #404041; text-transform: uppercase; font-weight: 700; } #wpfront-notification-bar-spacer #wpfront-notification-bar a { text-decoration: underline; } #wpfront-notification-bar-spacer .dialog-widget-content .dialog-close-button { display:none; } @media screen and (max-width: 767px) { #wpfront-notification-bar-spacer { /* TODO - figure this out */ } } /* Recent CSS updates */ #wpfront-notification-bar div.wpfront-message{ padding: 10px; } #wpfront-notification-bar-spacer #wpfront-notification-bar a { color: #ffffff; }/*]]>*/</style><div
id=wpfront-notification-bar-spacer class="wpfront-notification-bar-spacer  hidden"><div
id=wpfront-notification-bar-open-button aria-label=reopen role=button class="wpfront-notification-bar-open-button hidden top wpfront-bottom-shadow"></div><div
id=wpfront-notification-bar class="wpfront-notification-bar wpfront-fixed    top "><table
id=wpfront-notification-bar-table border=0 cellspacing=0 cellpadding=0 role=presentation><tr><td><div
class="wpfront-message wpfront-div">
Annual User Satisfaction Survey. We need your help to improve CIOOS Atlantic. <a
href=https://5vd1hix0m5v.typeform.com/to/acsUSp4i target=_blank rel=noopener>Take this 2-min survey.</a>
<br>Sondage de satisfaction annuel. Nous avons besoin de votre aide pour améliorer SIOOC Atlantique. <a
href=https://5vd1hix0m5v.typeform.com/to/ElvLIbsy target=_blank rel=noopener>Répondez à ce sondage de moins de 2 minutes.</a></div></td></tr></table></div></div> 
<script>function __load_wpfront_notification_bar() {
                    if (typeof wpfront_notification_bar === "function") {
                        wpfront_notification_bar({"position":1,"height":0,"fixed_position":false,"animate_delay":0.5,"close_button":false,"button_action_close_bar":false,"auto_close_after":0,"display_after":1,"is_admin_bar_showing":false,"display_open_button":false,"keep_closed":false,"keep_closed_for":0,"position_offset":0,"display_scroll":false,"display_scroll_offset":100,"keep_closed_cookie":"wpfront-notification-bar-keep-closed","log":false,"id_suffix":"","log_prefix":"[WPFront Notification Bar]","theme_sticky_selector":"","set_max_views":false,"max_views":0,"max_views_for":0,"max_views_cookie":"wpfront-notification-bar-max-views"});
                    } else {
                                    setTimeout(__load_wpfront_notification_bar, 100);
                    }
                }
                __load_wpfront_notification_bar();</script> <div
id=page class=site>

<header
id=masthead class=page-header><div
class=pre-nav><div
class=container><div
class=nationallogo><img
class=lazy alt="CIOOS National" src="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201%201'%3E%3C/svg%3E" data-src=https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/CIOOS-watermark.svg?x48800></div><div
class=logotype><aside
class="text-3 widget widget_text"><div
class=textwidget><p><a
href=https://cioos.ca/ >A Regional Association of CIOOS</a></p></div></aside></div></div></div><div
class=post-nav><div
class=container><div
class=sitelogo>
<a
rel=home href=/ ><img
class=lazy src="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201%201'%3E%3C/svg%3E" data-src=https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg?x48800 alt="CIOOS Atlantic"></a></div><nav
id=site-navigation class="site-nav nav main-nav main-navigation">
<button
class=menu-toggle aria-controls=primary-menu aria-expanded=false>Primary Menu</button><div
class=menu-main-menu-en-container><ul
id=primary-menu class=menu><li
id=menu-item-1469 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home menu-item-1469"><a
href=https://cioosatlantic.ca/ >Home</a></li>
<li
id=menu-item-1467 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-1467"><a
href=https://cioosatlantic.ca/about/ >About</a><ul
class=sub-menu>
<li
id=menu-item-1473 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1473"><a
href=https://cioosatlantic.ca/about/ >About CIOOS Atlantic</a></li>
<li
id=menu-item-2811 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2811"><a
href=https://cioosatlantic.ca/cioos-atlantic-team/ >Meet Our Team</a></li>
<li
id=menu-item-2830 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2830"><a
href=https://cioosatlantic.ca/our-partners/ >Our Partners</a></li>
<li
id=menu-item-1468 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1468"><a
href=https://cioosatlantic.ca/partnership-profiles/ >Partnership Profiles</a></li></ul>
</li>
<li
id=menu-item-2794 class="menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-2787 current_page_item menu-item-has-children menu-item-2794"><a
href=https://cioosatlantic.ca/data-tools/ aria-current=page>Data Tools</a><ul
class=sub-menu>
<li
id=menu-item-2866 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2866"><a
href=https://assetmap.cioosatlantic.ca>Asset Map</a></li>
<li
id=menu-item-3263 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3263"><a
href=https://cioosatlantic.ca/cmar/BirchyHead/ >CMAR Birchy Head Visualization</a></li>
<li
id=menu-item-3264 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3264"><a
href=https://cioosatlantic.ca/cmar/ShipHarbour/ >CMAR Ship Harbour Visualization</a></li>
<li
id=menu-item-3265 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-3265"><a
href=https://cioosatlantic.ca/erddap>ERDDAP Data Access</a></li></ul>
</li>
<li
id=menu-item-2781 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-2781"><a
href=https://catalogue.cioosatlantic.ca/ >Data Catalogue</a><ul
class=sub-menu>
<li
id=menu-item-2782 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2782"><a
href=https://catalogue.cioosatlantic.ca/en/dataset>Datasets</a></li>
<li
id=menu-item-2783 class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2783"><a
href=https://catalogue.cioosatlantic.ca/en/organization>Organizations</a></li></ul>
</li>
<li
id=menu-item-1510 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-1510"><a
href=https://cioosatlantic.ca/resources/ >Resources</a><ul
class=sub-menu>
<li
id=menu-item-1485 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1485"><a
href=https://cioosatlantic.ca/essential-ocean-variables/ >Essential Ocean Variables</a></li>
<li
id=menu-item-2825 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2825"><a
href=https://cioosatlantic.ca/data-management/ >Data Management</a></li>
<li
id=menu-item-1511 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1511"><a
href=https://cioosatlantic.ca/resources/ >Resources</a></li>
<li
id=menu-item-2836 class="menu-item menu-item-type-post_type menu-item-object-page menu-item-2836"><a
href=https://cioosatlantic.ca/webinars-and-discussions/ >Webinars and Discussions</a></li></ul>
</li></ul></div></nav><nav
id=language class="site-nav nav language-nav"><div
class=menu-default-container><ul
class=sitelanguages>
<li
class="lang-item lang-item-5 lang-item-fr lang-item-first"><a
lang=fr-CA hreflang=fr-CA href=https://cioosatlantic.ca/fr/outils/ >fr</a></li></ul></div></nav></div></div></header>

    {% block inner_body %}
    {% block contents %}
        {% for doc in docs %}
        {{ embed(doc) if doc.elementid }}
        {% for root in doc.roots %}
            {{ embed(root) | indent(10) }}
        {% endfor %}
        {% endfor %}
    {% endblock %}
    {{ plot_script | indent(8) }}
    {% endblock %}

<footer
id=colophon class=site-footer><div
class=container><div
class=col><aside
class="text-10 widget widget_text">CONTACT US<div
class=textwidget><p><a
href=https://twitter.com/CIOOSAtlantic>Twitter</a><br>
<a
href=https://www.linkedin.com/company/cioosatlantic/ >LinkedIn</a><br>
<a
href=mailto:info@cioosatlantic.ca>Contact Us</a><br>
<a
href=https://cioosatlantic.ca/opportunities/ >Opportunities</a></p></div></aside></div><div
class=col><aside
class="widget_text custom_html-4 widget widget_custom_html">CIOOS<div
class="textwidget custom-html-widget"><a
href=https://cioos.ca>CIOOS National</a><br>
<a
href=https://cioospacific.ca/ >Pacific Region</a><br>
<a
href=https://slgo.ca/en/ >St. Lawrence Region</a><br>
<a
href=https://cioosatlantic.ca>Atlantic Region</a></div></aside></div><div
class=col><aside
class="widget_text custom_html-6 widget widget_custom_html">DATA<div
class="textwidget custom-html-widget"><a
href=https://catalogue.cioosatlantic.ca/ >Catalogue</a><br>
<a
href=https://assetmap.cioosatlantic.ca/ >Asset Map</a></div></aside></div><div
class=col><aside
class="text-8 widget widget_text">Subscribe to our Newsletter<div
class=textwidget><p></p><div
class=mailchimp-form><form
id=mc-embedded-subscribe-form class=validate action="https://cioosatlantic.us19.list-manage.com/subscribe/post?u=70e43ded9ed1212de9f9d02fc&amp;id=b6549cddce" method=post name=mc-embedded-subscribe-form novalidate target=_blank><input
id=mce-FNAME class=newsletter-field name=FNAME type=text value placeholder="First name"><br>
<input
id=mce-EMAIL class="required email newsletter-field" name=EMAIL type=email value placeholder="Email address"></p><div
id=mce-responses class=clear><div
id=mce-error-response class=response style="display: none;"></div><div
id=mce-success-response class=response style="display: none;"></div></div><p></p><div
style="position: absolute; left: -5000px;" aria-hidden=true><input
tabindex=-1 name=b_70e43ded9ed1212de9f9d02fc_b6549cddce type=text value></div><p><input
id=mc-embedded-subscribe class="btn btn--solid" name=subscribe type=submit value=Subscribe></p></form></div><p></p></div></aside></div></div></footer>
</div>

<svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-dark-grayscale><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0 0.49803921568627"/><feFuncG
type="table" tableValues="0 0.49803921568627"/><feFuncB
type="table" tableValues="0 0.49803921568627"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-grayscale><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0 1"/><feFuncG
type="table" tableValues="0 1"/><feFuncB
type="table" tableValues="0 1"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-purple-yellow><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0.54901960784314 0.98823529411765"/><feFuncG
type="table" tableValues="0 1"/><feFuncB
type="table" tableValues="0.71764705882353 0.25490196078431"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-blue-red><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0 1"/><feFuncG
type="table" tableValues="0 0.27843137254902"/><feFuncB
type="table" tableValues="0.5921568627451 0.27843137254902"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-midnight><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0 0"/><feFuncG
type="table" tableValues="0 0.64705882352941"/><feFuncB
type="table" tableValues="0 1"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-magenta-yellow><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0.78039215686275 1"/><feFuncG
type="table" tableValues="0 0.94901960784314"/><feFuncB
type="table" tableValues="0.35294117647059 0.47058823529412"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-purple-green><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0.65098039215686 0.40392156862745"/><feFuncG
type="table" tableValues="0 1"/><feFuncB
type="table" tableValues="0.44705882352941 0.4"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><svg
xmlns=http://www.w3.org/2000/svg viewBox="0 0 0 0" width=0 height=0 focusable=false role=none style="visibility: hidden; position: absolute; left: -9999px; overflow: hidden;" ><defs><filter
id=wp-duotone-blue-orange><feColorMatrix
color-interpolation-filters="sRGB" type="matrix" values=" .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 .299 .587 .114 0 0 "/><feComponentTransfer
color-interpolation-filters="sRGB" ><feFuncR
type="table" tableValues="0.098039215686275 1"/><feFuncG
type="table" tableValues="0 0.66274509803922"/><feFuncB
type="table" tableValues="0.84705882352941 0.41960784313725"/><feFuncA
type="table" tableValues="1 1"/></feComponentTransfer><feComposite
in2="SourceGraphic" operator="in"/></filter></defs></svg><script src=https://cioosatlantic.ca/wp-content/cache/minify/7490b.js?x48800></script> <script>(function() {
				var expirationDate = new Date();
				expirationDate.setTime( expirationDate.getTime() + 31536000 * 1000 );
				document.cookie = "pll_language=en; expires=" + expirationDate.toUTCString() + "; path=/; secure; SameSite=Lax";
			}());</script> <script>window.w3tc_lazyload=1,window.lazyLoadOptions={elements_selector:".lazy",callback_loaded:function(t){var e;try{e=new CustomEvent("w3tc_lazyload_loaded",{detail:{e:t}})}catch(a){(e=document.createEvent("CustomEvent")).initCustomEvent("w3tc_lazyload_loaded",!1,!1,{e:t})}window.dispatchEvent(e)}}</script><script async src=https://cioosatlantic.ca/wp-content/cache/minify/1615d.js?x48800></script>
</body>
{% endblock %}
'''

pn.extension(sizing_mode='stretch_width')


import pandas as pd
import os
from erddapy import ERDDAP
import numpy as np

IDlist = ['wpsu-7fer','knwz-4bap',
                  'eb3n-uxcb','x9dy-aai9','a9za-3t63','eda5-aubu','adpu-nyt8','v6sa-tiit','mq2k-54s4','9qw2-yb2f']

IDlist = ['wpsu-7fer']

stationdict = {}
e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
for val in IDlist:
    e.dataset_id = val
    e.variables = ['waterbody_station']
    df = e.to_pandas()
    df.waterbody_station= df.waterbody_station.astype(str)
    stations = sorted(list(df.waterbody_station.unique()))
    for i in range(len(stations)):
        stationdict[stations[i]]= val

stationlist = list(stationdict.keys())
        


# In[3]:


def getdata(station_name):
    e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
    e.auth = ("cioosatlantic", "4oceans")
    e.response = "csv"
    e.variables = ['waterbody_station', 'latitude', 'longitude', 'time', 'Temperature', 'Dissolved_Oxygen', 'depth']
    e.dataset_id = stationdict.get(station_name)
    e.constraints = {"waterbody_station=":station_name}
    df = e.to_pandas()
    df = df.sort_values(by=['time (UTC)'])
    df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
    df = df.set_index(df['time (UTC)'].astype(np.datetime64))
    df['DO mg/L']  = ((df['Temperature (degrees Celsius)']*0.0026)**2-(df['Temperature (degrees Celsius)']*0.2567)+11.698)*(df['Dissolved_Oxygen (% saturation)']/100)
    df = df.rename(columns={'depth (m)': "depth"})
    df = df.rename(columns={'latitude (degrees_north)': "latitude"})
    df = df.rename(columns={'longitude (degrees_east)': "longitude"})
    df = df.rename(columns={'Temperature (degrees Celsius)':'Temperature'})
    df = df.rename(columns={'Dissolved_Oxygen (% saturation)': 'DO %'})
    df.depth= df.depth.astype('category')
    
    return df



import panel as pn
import holoviews as hv
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import CategoricalColorMapper
from datashader.colors import Greys9, Hot, Elevation, Sets1to3
import datashader as ds
import holoviews.operation.datashader as hd
import hvplot.pandas


hv.extension("bokeh")


depthlist = list(range(1,32))
varlist = ['Temperature (degrees Celsius)', 'Dissolved_Oxygensizing_mode (% saturation)']

station_selector = pn.widgets.Select(name="Select Station", options = stationlist, value=stationlist[0])

############################################################################################################
tileopts = hv.opts.Tiles(projection=True)
tiles = hv.element.tiles.EsriImagery().opts(tileopts)

def geoplot(station_name):
    data = getdata(station_name)
    locations = data.groupby('waterbody_station')['longitude', 'latitude'].mean()
    x, y = ds.utils.lnglat_to_meters(locations.longitude, locations.latitude)
    stationlocation = locations.assign(x=x,y=y)
    plotlocs = stationlocation.hvplot.points('x','y',hover_cols=['waterbody_station'], responsive=True).opts(color='red')
    mapplot = (plotlocs).options(xlim=(-7.05e6, -7e6), ylim=(5.2e6, 6e6), aspect='equal', xaxis=None,yaxis=None,
                                      active_tools=['pan', 'wheel_zoom'], toolbar=None)
    return mapplot

def updategeo(target, event):
    target.object = geoplot(event.new)
    
geopane = pn.pane.HoloViews(geoplot(station_selector.value), sizing_mode='stretch_both', background='#dbefe1')

station_selector.link(geopane, callbacks ={"value":updategeo})
###########################################################################################################
opts = dict(show_grid=True, 
            xformatter=DatetimeTickFormatter(months='%b %Y' ,days="%b/%d",hours="%H:%M",minutes="%H:%M"), tools = ["hover"], bgcolor='white')

colors = Elevation+Hot+Greys9+Sets1to3[0:5]
colorkey = dict(zip(depthlist, colors))

def plot(station_name):
    data = getdata(station_name)
    plottemp = data.hvplot.points(x='time (UTC)', y='Temperature', c='depth', color_key = colorkey, 
                                   datashade=True, aggregator= ds.count_cat('depth'), responsive=True).opts(**opts)
    
    spreadtemp = hd.dynspread(plottemp, threshold=.999, max_px=2).opts(bgcolor='white', show_grid=True,tools = ["hover"],alpha=1)
    plotoxy = data.hvplot.points(x='time (UTC)',y= 'DO mg/L' , c='depth', color_key = colorkey, datashade=True, responsive=True,
        aggregator= ds.count_cat('depth') ).opts(**opts)
    spreadoxy = hd.dynspread(plotoxy, threshold=.999, max_px=2).opts(bgcolor='white', show_grid=True,tools = ["hover"],alpha=1)
    #oxylimit1 = hv.HLine(6).opts(color='red', line_dash='dashed', line_width=4.0)*hv.Text(data['time (UTC)'].median(),6.2, "oxygen limit for x" )
    oxyspan = hv.HSpan(0,6).opts(fill_color='red' )
    tempspan = hv.HSpan(-100, -0.7).opts(fill_color='blue', alpha=0.5)
    
    plots = (spreadtemp*tempspan+spreadoxy*oxyspan).opts(shared_axes=True, toolbar='right')
    return plots.cols(1)


def updatestation(target, event):
    plotpane.loading = True
    target.object = plot(event.new)
    plotpane.loading = False


plotpane = pn.pane.HoloViews(plot(station_selector.value) ,background='#dbefe1')

station_selector.link(plotpane, callbacks={"value":updatestation})

########################################################################################################
def title(station_name):
    title = station_name
    return title

def updatetitle(target, event):
    target.object = title(event.new)

titlepane = pn.pane.Markdown(title(station_selector.value), align='center',style={'font-size':'40px', 'font-family':'Quicksand'}, background='#dbefe1')

station_selector.link(titlepane, callbacks = {"value":updatetitle})

if os.path.exists("CMARlogo.png"):
    cmarlogo = pn.panel("CMARlogo.png")

if os.path.exists("canadamap.png"):
    canadamap = pn.panel("canadamap.png")
#'No machine-readable author provided. Golbez assumed (based on copyright claims)., CC BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>, via Wikimedia Commons'

if os.path.exists("tempsensor.png"):
    oxysensor = pn.panel("oxysensor.png")
# Adapted from https://www.innovasea.com/wp-content/uploads/2021/10/Innovasea-Aquaculture-Intelligence-Spec-Sheet.pdf

if os.path.exists("tempsensor.png"):
    tempsensor = pn.panel("tempsensor.png")

widgets = pn.WidgetBox(pn.Column(station_selector),align = 'center')

gspec = pn.GridSpec(sizing_mode='stretch_both', background='#dbefe1')

gspec[:2,  0] = canadamap
#gspec[2:4, 0] = geopane
gspec[5,   0] = cmarlogo

gspec[0, 1:3] = titlepane
gspec[1, 1:3] = widgets
gspec[2:6, 1:3] = plotpane

gspec[0:2, 3] = pn.Spacer(background='#dbefe1', margin=5)
gspec[2:4, 3] = oxysensor
gspec[4:6, 3] = tempsensor


gspec = pn.GridSpec(sizing_mode='stretch_both')

gspec[:,   0  ] = pn.Spacer(background='red',    margin=1)
gspec[0,   1:3] = pn.Spacer(background='green',  margin=1)
gspec[1,   2:4] = pn.Spacer(background='orange', margin=1)
gspec[2,   1:4] = pn.Spacer(background='blue',   margin=1)
gspec[0:1, 3:4] = pn.Spacer(background='purple', margin=1)

gspec

dashboard = gspec

tmpl = pn.template.Template(template)
tmpl.add_panel('A', dashboard)
tmpl.servable()
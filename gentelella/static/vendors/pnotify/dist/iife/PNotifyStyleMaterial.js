var _typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},_extends=Object.assign||function(t){for(var i=1;i<arguments.length;i++){var o=arguments[i];for(var n in o)Object.prototype.hasOwnProperty.call(o,n)&&(t[n]=o[n])}return t},PNotifyStyleMaterial=function(t){"use strict";function i(){var t=function(t){return document.createElement(t)}("style");t.id="svelte-19og8nx-style",t.textContent='[ui-pnotify] .pnotify-material{-webkit-border-radius:0;-moz-border-radius:0;border-radius:0;font-size:14px}[ui-pnotify] .pnotify-material.ui-pnotify-shadow{-webkit-box-shadow:0px 6px 24px 0px rgba(0,0,0,0.2);-moz-box-shadow:0px 6px 24px 0px rgba(0,0,0,0.2);box-shadow:0px 6px 24px 0px rgba(0,0,0,0.2)}[ui-pnotify] .pnotify-material.ui-pnotify-container{padding:24px}[ui-pnotify] .pnotify-material .ui-pnotify-title{font-size:20px;margin-bottom:20px;line-height:24px}[ui-pnotify] .pnotify-material .ui-pnotify-title:last-child{margin-bottom:0}[ui-pnotify] .pnotify-material .ui-pnotify-text{font-size:16px;line-height:24px}[ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-title,[ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-text,[ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-confirm{margin-left:32px}[dir=rtl] [ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-title,[dir=rtl] [ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-text,[dir=rtl] [ui-pnotify].ui-pnotify-with-icon .pnotify-material .ui-pnotify-confirm{margin-right:32px;margin-left:0}[ui-pnotify] .pnotify-material .ui-pnotify-action-bar{margin-top:20px;margin-right:-16px;margin-bottom:-16px}[dir=rtl] [ui-pnotify] .pnotify-material .ui-pnotify-action-bar{margin-left:-16px;margin-right:0}[ui-pnotify] .pnotify-material-notice{background-color:#FFEE58;border:none;color:#000}[ui-pnotify] .pnotify-material-info{background-color:#26C6DA;border:none;color:#000}[ui-pnotify] .pnotify-material-success{background-color:#66BB6A;border:none;color:#fff}[ui-pnotify] .pnotify-material-error{background-color:#EF5350;border:none;color:#fff}[ui-pnotify] .pnotify-material-icon-notice,[ui-pnotify] .pnotify-material-icon-info,[ui-pnotify] .pnotify-material-icon-success,[ui-pnotify] .pnotify-material-icon-error,[ui-pnotify] .pnotify-material-icon-closer,[ui-pnotify] .pnotify-material-icon-sticker{position:relative}[ui-pnotify] .pnotify-material-icon-closer,[ui-pnotify] .pnotify-material-icon-sticker{height:20px;width:20px;font-size:20px;line-height:20px;position:relative}[ui-pnotify] .pnotify-material-icon-notice:after,[ui-pnotify] .pnotify-material-icon-info:after,[ui-pnotify] .pnotify-material-icon-success:after,[ui-pnotify] .pnotify-material-icon-error:after,[ui-pnotify] .pnotify-material-icon-closer:after,[ui-pnotify] .pnotify-material-icon-sticker:after{font-family:\'Material Icons\'}[ui-pnotify] .pnotify-material-icon-notice:after{content:"announcement"}[ui-pnotify] .pnotify-material-icon-info:after{content:"info"}[ui-pnotify] .pnotify-material-icon-success:after{content:"check_circle"}[ui-pnotify] .pnotify-material-icon-error:after{content:"error"}[ui-pnotify] .pnotify-material-icon-closer,[ui-pnotify] .pnotify-material-icon-sticker{display:inline-block}[ui-pnotify] .pnotify-material-icon-closer:after{top:-4px;content:"close"}[ui-pnotify] .pnotify-material-icon-sticker:after{top:-5px;content:"pause"}[ui-pnotify] .pnotify-material-icon-sticker.pnotify-material-icon-stuck:after{content:"play_arrow"}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-prompt-input{display:block;width:100%;margin-bottom:8px;padding:15px 0 8px;background-color:transparent;color:inherit;border-radius:0;border-top:none;border-left:none;border-right:none;border-bottom-style:solid;border-bottom-color:inherit;border-bottom-width:1px}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-prompt-input:focus{outline:none;border-bottom-color:#3F51B5;border-bottom-width:2px}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button{position:relative;padding:0 16px;overflow:hidden;border-width:0;outline:none;border-radius:2px;background-color:transparent;color:inherit;transition:background-color .3s;text-transform:uppercase;height:36px;margin:6px;min-width:64px;font-weight:bold}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button.ui-pnotify-material-primary{color:#3F51B5}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button:hover,[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button:focus{background-color:rgba(0, 0, 0, .12);color:inherit}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button.ui-pnotify-material-primary:hover,[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button.ui-pnotify-material-primary:focus{color:#303F9F}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button:before{content:"";position:absolute;top:50%;left:50%;display:block;width:0;padding-top:0;border-radius:100%;background-color:rgba(153, 153, 153, .4);-webkit-transform:translate(-50%, -50%);-moz-transform:translate(-50%, -50%);-ms-transform:translate(-50%, -50%);-o-transform:translate(-50%, -50%);transform:translate(-50%, -50%)}[ui-pnotify].ui-pnotify .pnotify-material .ui-pnotify-action-button:active:before{width:120%;padding-top:120%;transition:width .2s ease-out, padding-top .2s ease-out}',function(t,i){t.appendChild(i)}(document.head,t)}function o(t){!function(t,i){t._handlers=a(),t._slots=a(),t._bind=i._bind,t._staged={},t.options=i,t.root=i.root||t,t.store=i.store||t.root.store,i.root||(t._beforecreate=[],t._oncreate=[],t._aftercreate=[])}(this,t),this._state=e({},t.data),this._intro=!0,document.getElementById("svelte-19og8nx-style")||i(),this._fragment=(this._state,{c:r,m:r,p:r,d:r}),t.target&&(this._fragment.c(),this._mount(t.target,t.anchor))}var n;function r(){}function e(t,i){for(var o in i)t[o]=i[o];return t}function a(){return Object.create(null)}function f(t){for(;t&&t.length;)t.shift()()}return t=t&&t.__esModule?t.default:t,e(o.prototype,{destroy:function(t){this.destroy=r,this.fire("destroy"),this.set=r,this._fragment.d(!1!==t),this._fragment=null,this._state={}},get:function(){return this._state},fire:function(t,i){var o=t in this._handlers&&this._handlers[t].slice();if(!o)return;for(var n=0;n<o.length;n+=1){var r=o[n];if(!r.__calling)try{r.__calling=!0,r.call(this,i)}finally{r.__calling=!1}}},on:function(t,i){var o=this._handlers[t]||(this._handlers[t]=[]);return o.push(i),{cancel:function(){var t=o.indexOf(i);~t&&o.splice(t,1)}}},set:function(t){if(this._set(e({},t)),this.root._lock)return;!function(t){t._lock=!0,f(t._beforecreate),f(t._oncreate),f(t._aftercreate),t._lock=!1}(this.root)},_set:function(t){var i=this._state,o={},n=!1;for(var r in t=e(this._staged,t),this._staged={},t)this._differs(t[r],i[r])&&(o[r]=n=!0);if(!n)return;this._state=e(e({},i),t),this._recompute(o,this._state),this._bind&&this._bind(o,this._state);this._fragment&&(this.fire("state",{changed:o,current:this._state,previous:i}),this._fragment.p(o,this._state),this.fire("update",{changed:o,current:this._state,previous:i}))},_stage:function(t){e(this._staged,t)},_mount:function(t,i){this._fragment[this._fragment.i?"i":"m"](t,i||null)},_differs:function(t,i){return t!=t?i==i:t!==i||t&&"object"===(void 0===t?"undefined":_typeof(t))||"function"==typeof t}}),o.prototype._recompute=r,(n=o).key="StyleMaterial",t.modules.StyleMaterial=n,t.modulesPrependContainer.push(n),t.styling.material||(t.styling.material={}),t.styling.material=_extends(t.styling.material,{container:"pnotify-material",notice:"pnotify-material-notice",info:"pnotify-material-info",success:"pnotify-material-success",error:"pnotify-material-error"}),t.icons.material||(t.icons.material={}),t.icons.material=_extends(t.icons.material,{notice:"material-icons pnotify-material-icon-notice",info:"material-icons pnotify-material-icon-info",success:"material-icons pnotify-material-icon-success",error:"material-icons pnotify-material-icon-error",closer:"material-icons pnotify-material-icon-closer",pinUp:"material-icons pnotify-material-icon-sticker",pinDown:"material-icons pnotify-material-icon-sticker pnotify-material-icon-stuck"}),o}(PNotify);
//# sourceMappingURL=PNotifyStyleMaterial.js.map
import { LightningElement } from 'lwc';

export default class CssCommonElement extends LightningElement {
    _bootstrapCss() {
        let _bootstrap = '../bootstrap/css/bootstrap.min.css';
        const styles = document.createElement('link');
        styles.href = _bootstrap;
        styles.rel = 'stylesheet';
        return styles;
    }

    _createScriptTag(src) {
        const script = document.createElement('script');
        script.src = src;
        script.type = 'text/javascript';
        return script;
    }

    _jqueryJs() {
        return this._createScriptTag('../jquery/jquery.min.js');
    }

    _bootstrapJs() {
        return this._createScriptTag('../bootstrap/js/bootstrap.bundle.min.js');
    }

    constructor() {
        super();
        this.template.appendChild(this._bootstrapCss());
        this.template.appendChild(this._jqueryJs());
        setTimeout(() => {
            this.template.appendChild(this._bootstrapJs());
        }, 100);
    }
}

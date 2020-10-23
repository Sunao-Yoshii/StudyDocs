import { api } from 'lwc';
import CssCommonElement from 'todo/cssCommon';

export default class SubComponent extends CssCommonElement {
    @api title;
}

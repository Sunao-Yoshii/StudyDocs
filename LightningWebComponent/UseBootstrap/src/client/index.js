import { createElement } from 'lwc';
import TodoApp from 'todo/app';

const app = createElement('todo-app', { is: TodoApp });
// eslint-disable-next-line @lwc/lwc/no-document-query
document.querySelector('#main').appendChild(app);

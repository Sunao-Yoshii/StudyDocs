class Hoge {
	constructor() {
		this.message = 'Hello class';
	}
	hello() {
		return this.message;
	}
}

let hoge = new Hoge();
alert(hoge.hello());
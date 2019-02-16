import UIKit

struct Person {
    var firstName: String
    var lastName: String
    func sayHello() {
        print("Hello there! My name is \(firstName) \(lastName).")
    }
}

let aPerson = Person(firstName: "Jacob", lastName: "Edwards")
let anotherPerson = Person(firstName: "Candace", lastName: "Salinas")
aPerson.sayHello()
anotherPerson.sayHello()

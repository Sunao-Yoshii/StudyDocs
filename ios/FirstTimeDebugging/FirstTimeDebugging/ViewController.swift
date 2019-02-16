import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var myButton: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let sample = "sample"
        print(sample)
    }
    
    func someMethod() {

    }

    @IBAction func onMyButtonPressed(_ sender: Any) {
        print("The button was pressed")
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}


//
//  ViewController.swift
//  InterfaceBuilderBasics
//
//  Created by 吉井温 on 2019/02/16.
//  Copyright © 2019 吉井温. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var mainLabvel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    @IBAction func changeTitle(_ sender: Any) {
        self.mainLabvel.text = "This app rocks!"
    }
}


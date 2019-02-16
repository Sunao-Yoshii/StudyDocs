//
//  ViewController.swift
//  Light
//
//  Created by 吉井温 on 2019/02/16.
//  Copyright © 2019 吉井温. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    var isLightOn = true

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
    }

    @IBAction func buttonPressed(_ sender: Any) {
        self.isLightOn = !self.isLightOn
        self.updateUiState()
    }
    
    func updateUiState() {
        self.view.backgroundColor = self.isLightOn ? .white : .black
    }
}


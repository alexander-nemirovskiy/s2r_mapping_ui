import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatRadioChange, } from '@angular/material/radio';

@Component({
  selector: 'mapping-selector',
  templateUrl: './mapping-selector.component.html',
  styleUrls: ['./mapping-selector.component.scss']
})
export class MappingSelectorComponent implements OnInit {
    private _custom_option = "";
    private selected_option = "";
    selector_form: FormGroup;
    temp_options = [
        {name: "first"},
        {name: "second"},
        {name: "third"},
        {name: "fourth"},
    ];

    constructor(private formBuilder: FormBuilder) { }

    ngOnInit(): void {
        this.selector_form = this.formBuilder.group({
            mapping_options: ['', Validators.required]
        });
    }
 
    mappingOption(event: any) {
        this._custom_option = event.target.value;
        this.selector_form.controls['mapping_options'].setValue('other')
    }

    onRadioChange(mrChange: MatRadioChange){
        this.selected_option = mrChange.value;
    }

    confirm(){
        // required otherwise the first call does not allow <input> to be
        // the value (nobody is setting selected_option)
        let value = this.selector_form.controls['mapping_options'].value
        // let value = this.selected_option
        if (this.isValid){
            if(value === "other"){
                console.log(`Form value: ${this._custom_option}`)
                return
            }
            console.log(`Form value: ${value}`);
        }
    }

    isValid(): boolean{
        let value = this.selector_form.controls['mapping_options'].value
        if(value === "other")
            return !(this._custom_option.length > 0)
        return !this.selector_form.valid 
    }

}

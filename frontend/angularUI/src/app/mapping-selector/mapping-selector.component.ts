import { Component, OnInit, Input } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatRadioChange, } from '@angular/material/radio';
import { MappingPair } from '../models/MappingPair';
import { LoggerService } from '../services/logger.service';

@Component({
  selector: 'mapping-selector',
  templateUrl: './mapping-selector.component.html',
  styleUrls: ['./mapping-selector.component.scss']
})
export class MappingSelectorComponent implements OnInit {
    @Input() mappingPair: MappingPair;

    private _custom_option = "";
    private selected_option = "";
    selector_form: FormGroup;

    constructor(private formBuilder: FormBuilder, private logger: LoggerService) { }

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
        let value = this.selector_form.controls['mapping_options'].value
        if (this.isValid){
            if(value === "other"){
                this.logger.log(`Form value: ${this._custom_option}`)
                return
            }
            this.logger.log(`Form value: ${value}`);
        }
    }

    isValid(): boolean{
        let value = this.selector_form.controls['mapping_options'].value
        if(value === "other")
            return !(this._custom_option.length > 0)
        return !this.selector_form.valid 
    }

}

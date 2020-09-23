import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatRadioChange, } from '@angular/material/radio';
import { MappingPair } from '../models/MappingPair';
import { LoggerService } from '../services/logger.service';
import { MappingService } from '../services/mapping.service';

@Component({
  selector: 'mapping-selector',
  templateUrl: './mapping-selector.component.html',
  styleUrls: ['./mapping-selector.component.scss']
})
export class MappingSelectorComponent implements OnInit {
    @Input() mappingPair: MappingPair;
    @Output() dismissEvent: EventEmitter<any> = new EventEmitter();

    private _custom_option = "";
    private selected_option = "";
    selector_form: FormGroup;
    public showSelector = true;

    constructor(
        private formBuilder: FormBuilder, 
        private mappingService: MappingService,
        private logger: LoggerService) { }

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

    confirmMapping(){
        let value = this.selector_form.controls['mapping_options'].value
        if (this.isValid){
            let v = ''
            if(value === "other"){
                v = this._custom_option;
                // this.logger.log(`Form value: ${this._custom_option}`)
                // m.mappingOptions.push(this._custom_option);
            }
            else {
                v = value;
                // this.logger.log(`Form value: ${value}`);
                // m.mappingOptions.push(value);
            }
            let m: MappingPair = new MappingPair(this.mappingPair.sourceTerm, [v]);
            this.mappingService.confirmMappingPair(m);
            this.logger.log(`Selection performed: [${v}]`);
            this.dismissEvent.emit(this.mappingPair);
        }
    }

    deleteMapping(){
        this.logger.log(`Option ${this.mappingPair.sourceTerm} was rejected.`);
        this.dismissEvent.emit(this.mappingPair);
    }

    isValid(): boolean{
        let value = this.selector_form.controls['mapping_options'].value
        if(value === "other")
            return !(this._custom_option.length > 0)
        return !this.selector_form.valid 
    }

}

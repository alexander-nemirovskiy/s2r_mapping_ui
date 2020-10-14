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
    public valid_selection = false;

    constructor(
        private formBuilder: FormBuilder, 
        private mappingService: MappingService,
        private logger: LoggerService) { }

    ngOnInit(): void {
        this.selector_form = this.formBuilder.group({
            mapping_options: ['', Validators.required]
        });
        let default_value = this.mappingPair.mappingOptions[0]
        this.selector_form.controls['mapping_options'].setValue(default_value)
        this.valid_selection = default_value.length > 0;
    }
 
    mappingOption(event: any) {
        this._custom_option = event.target.value;
        this.selector_form.controls['mapping_options'].setValue('other')
    }

    onRadioChange(mrChange: MatRadioChange){
        this.selected_option = mrChange.value;
        this.valid_selection = this.checkValidOptionSelected()
    }

    confirmMapping(){
        let value = this.selector_form.controls['mapping_options'].value
        this.logger.log(`Valid selection: ${this.checkValidOptionSelected()}`)
        if (this.checkValidOptionSelected()){
            let v = ''
            v = value === "other"? this._custom_option: value;
            let m: MappingPair = new MappingPair(this.mappingPair.sourceTerm, [v], [100]);
            this.mappingService.confirmMappingPair(m);
            this.logger.log(`Selection performed: [${v}]`);
            this.dismissEvent.emit(this.mappingPair);
        }
    }

    deleteMapping(){
        this.logger.log(`Option ${this.mappingPair.sourceTerm} was rejected.`);
        this.dismissEvent.emit(this.mappingPair);
    }

    private checkValidOptionSelected(): boolean{
        let value = this.selector_form.controls['mapping_options'].value
        if(value === "other"){
            this.logger.warn(`Output ${value}`)
            this.logger.warn(`Custom value ${this._custom_option} - ${this._custom_option.length > 0}`)
            return (this._custom_option.length > 0)
        }
        this.logger.warn(`Output ${value} - ${this.selector_form.valid}`)
        return this.selector_form.valid 
    }

}

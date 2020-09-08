import { MappingService } from './../services/mapping.service';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';
import { Observable } from 'rxjs';
import { MappingNotifierService } from '../services/mapping-notifier.service';
import { FileService } from '../services/file.service';

@Component({
    selector: 'file-select',
    templateUrl: './file-select.component.html',
    styleUrls: ['./file-select.component.scss'],
    providers: [{
        provide: STEPPER_GLOBAL_OPTIONS, useValue: {showError: true}
    }]
})
export class FileSelectComponent implements OnInit {
    @ViewChild('source_file_select') source_file_select;
    @ViewChild('target_file_select') target_file_select;

    public optionalFormGroup: FormGroup;
    public sourceFormGroup: FormGroup;
    public targetFormGroup: FormGroup;
    public selected_file: string
    public isOptional = true;
    
    sourceFiles$: Observable<string[]>;
    targetFiles$: Observable<string[]>;
    
    constructor(
        private _formBuilder: FormBuilder,
        private fileService: FileService,
        private notifier: MappingNotifierService) {}
    
    ngOnInit() {
        this.optionalFormGroup = this._formBuilder.group({
            optionalCtrl: ['']
        });
        this.sourceFormGroup = this._formBuilder.group({
            sourceFileControl: ['', Validators.required]
        });
        this.targetFormGroup = this._formBuilder.group({
            targetFileControl: ['', Validators.required]
        });
    }

    selectionChange($event){
        if($event.selectedStep === this.source_file_select){
            this.sourceFiles$ = this.fileService.getFiles('xml')
        }
        if($event.selectedStep === this.target_file_select){
            this.targetFiles$ = this.fileService.getFiles('ttl')
        }
    }

    startMapping(){
        // if (!this.sourceFormGroup.valid){
        //     return;
        // }
        // else {
        //     console.log('Yay!');
        //     this.notifier.notify();
        // }
        // TODO remove
        console.log('Nay!');
        this.notifier.notify();
    }
}

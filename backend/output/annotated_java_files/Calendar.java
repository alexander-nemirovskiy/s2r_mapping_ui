package com.example.jaxb.generated;

import java.util.List;

import com.example.jaxb.generated.Gtfs.Calendar.Service;

public class Calendar {
	@XmlElement(required = true)
	private List<Service> service;

	public Calendar() {
	}

	public List<Service> getService() {
		return service;
	}

	public void setService(List<Service> service) {
		this.service = service;
	}
}
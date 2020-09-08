package com.example.jaxb.generated;

@RdfsClass("gtfs:Service")
//@RdfProperty(propertyName = "gtfs:serviceRule")
//@RdfProperty(propertyName = "gtfs:service")
public class Service {
	@RdfProperty(propertyName = "gtfs:longName")
	//@RdfsClass("gtfs:PickupType")
	@XmlAttribute(name = "service_id", required = true)
	private String serviceId;
	@XmlSchemaType(name = "unsignedByte")
	@RdfProperty(propertyName = "gtfs:monday")
	@RdfProperty(propertyName = "gtfs:thursday")
	@RdfProperty(propertyName = "gtfs:wednesday")
	@RdfProperty(propertyName = "gtfs:sunday")
	@RdfProperty(propertyName = "gtfs:saturday")
	@RdfProperty(propertyName = "gtfs:tuesday")
	@RdfProperty(propertyName = "gtfs:friday")
	@XmlAttribute(name = "monday", required = true)
	private short monday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "tuesday", required = true)
	private short tuesday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "wednesday", required = true)
	private short wednesday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "thursday", required = true)
	private short thursday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "friday", required = true)
	private short friday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "saturday", required = true)
	private short saturday;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "sunday", required = true)
	private short sunday;
	@XmlSchemaType(name = "unsignedInt")
	@RdfProperty(propertyName = "gtfs:startTime")
	@XmlAttribute(name = "start_date", required = true)
	private long startDate;
	@XmlSchemaType(name = "unsignedInt")
	@RdfProperty(propertyName = "gtfs:endTime")
	@XmlAttribute(name = "end_date", required = true)
	private long endDate;

	public Service() {
	}

	public String getServiceId() {
		return serviceId;
	}

	public void setServiceId(String serviceId) {
		this.serviceId = serviceId;
	}

	public short getMonday() {
		return monday;
	}

	public void setMonday(short monday) {
		this.monday = monday;
	}

	public short getTuesday() {
		return tuesday;
	}

	public void setTuesday(short tuesday) {
		this.tuesday = tuesday;
	}

	public short getWednesday() {
		return wednesday;
	}

	public void setWednesday(short wednesday) {
		this.wednesday = wednesday;
	}

	public short getThursday() {
		return thursday;
	}

	public void setThursday(short thursday) {
		this.thursday = thursday;
	}

	public short getFriday() {
		return friday;
	}

	public void setFriday(short friday) {
		this.friday = friday;
	}

	public short getSaturday() {
		return saturday;
	}

	public void setSaturday(short saturday) {
		this.saturday = saturday;
	}

	public short getSunday() {
		return sunday;
	}

	public void setSunday(short sunday) {
		this.sunday = sunday;
	}

	public long getStartDate() {
		return startDate;
	}

	public void setStartDate(long startDate) {
		this.startDate = startDate;
	}

	public long getEndDate() {
		return endDate;
	}

	public void setEndDate(long endDate) {
		this.endDate = endDate;
	}
}
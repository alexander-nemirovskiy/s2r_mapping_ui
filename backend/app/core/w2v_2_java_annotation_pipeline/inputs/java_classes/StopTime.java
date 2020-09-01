package com.example.jaxb.generated;

import javax.xml.datatype.XMLGregorianCalendar;

public class StopTime {
	@XmlAttribute(name = "trip_id", required = true)
	private String tripId;
	@XmlSchemaType(name = "time")
	@XmlAttribute(name = "arrival_time", required = true)
	private XMLGregorianCalendar arrivalTime;
	@XmlSchemaType(name = "time")
	@XmlAttribute(name = "departure_time", required = true)
	private XMLGregorianCalendar departureTime;
	@XmlAttribute(name = "stop_id", required = true)
	private String stopId;
	@XmlSchemaType(name = "unsignedShort")
	@XmlAttribute(name = "stop_sequence", required = true)
	private int stopSequence;
	@XmlAttribute(name = "stop_headsign")
	private String stopHeadsign;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "pickup_type")
	private Short pickupType;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "drop_off_type")
	private Short dropOffType;
	@XmlAttribute(name = "shape_dist_traveled")
	private Double shapeDistTraveled;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "timepoint")
	private Short timepoint;

	public StopTime() {
	}

	public String getTripId() {
		return tripId;
	}

	public void setTripId(String tripId) {
		this.tripId = tripId;
	}

	public XMLGregorianCalendar getArrivalTime() {
		return arrivalTime;
	}

	public void setArrivalTime(XMLGregorianCalendar arrivalTime) {
		this.arrivalTime = arrivalTime;
	}

	public XMLGregorianCalendar getDepartureTime() {
		return departureTime;
	}

	public void setDepartureTime(XMLGregorianCalendar departureTime) {
		this.departureTime = departureTime;
	}

	public String getStopId() {
		return stopId;
	}

	public void setStopId(String stopId) {
		this.stopId = stopId;
	}

	public int getStopSequence() {
		return stopSequence;
	}

	public void setStopSequence(int stopSequence) {
		this.stopSequence = stopSequence;
	}

	public String getStopHeadsign() {
		return stopHeadsign;
	}

	public void setStopHeadsign(String stopHeadsign) {
		this.stopHeadsign = stopHeadsign;
	}

	public Short getPickupType() {
		return pickupType;
	}

	public void setPickupType(Short pickupType) {
		this.pickupType = pickupType;
	}

	public Short getDropOffType() {
		return dropOffType;
	}

	public void setDropOffType(Short dropOffType) {
		this.dropOffType = dropOffType;
	}

	public Double getShapeDistTraveled() {
		return shapeDistTraveled;
	}

	public void setShapeDistTraveled(Double shapeDistTraveled) {
		this.shapeDistTraveled = shapeDistTraveled;
	}

	public Short getTimepoint() {
		return timepoint;
	}

	public void setTimepoint(Short timepoint) {
		this.timepoint = timepoint;
	}
}
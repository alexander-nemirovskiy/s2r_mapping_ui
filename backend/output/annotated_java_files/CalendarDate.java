package com.example.jaxb.generated;

public class CalendarDate {
	@XmlAttribute(name = "service_id", required = true)
	private String serviceId;
	@XmlSchemaType(name = "unsignedInt")
	@XmlAttribute(name = "date", required = true)
	private long date;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "exception_type", required = true)
	private short exceptionType;

	public CalendarDate() {
	}

	public String getServiceId() {
		return serviceId;
	}

	public void setServiceId(String serviceId) {
		this.serviceId = serviceId;
	}

	public long getDate() {
		return date;
	}

	public void setDate(long date) {
		this.date = date;
	}

	public short getExceptionType() {
		return exceptionType;
	}

	public void setExceptionType(short exceptionType) {
		this.exceptionType = exceptionType;
	}
}
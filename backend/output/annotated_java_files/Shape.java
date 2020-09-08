package com.example.jaxb.generated;

import java.util.List;

import com.example.jaxb.generated.Gtfs.Shapes.Shape.ShapePt;

//@RdfProperty(propertyName = "gtfs:shape")
public class Shape {
	@XmlElement(name = "shape_pt", required = true)
	private List<ShapePt> shapePt;
	@XmlAttribute(name = "shape_id", required = true)
	private String shapeId;

	public Shape() {
	}

	public List<ShapePt> getShapePt() {
		return shapePt;
	}

	public void setShapePt(List<ShapePt> shapePt) {
		this.shapePt = shapePt;
	}

	public String getShapeId() {
		return shapeId;
	}

	public void setShapeId(String shapeId) {
		this.shapeId = shapeId;
	}
}
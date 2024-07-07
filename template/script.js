// app.js

// Convert the data into a hierarchy
const hierarchyData = d3.hierarchy(data, (d) => d.requirements);

let treeLayerWidths = {};
countLayerWidths(1, data);
const maxTreeWidth = Math.max(...Object.values(treeLayerWidths));

// Set canvas dimensions
const canvasWidth = 1000;
const canvasHeight = 250 + 150 * maxTreeWidth;

// Select the body element and append an SVG container
const mainSvg = d3
  .select("div.container")
  .append("svg")
  .attr("width", canvasWidth)
  .attr("height", canvasHeight);

const margin = 100;

// Adjust the mainSvg to add some margins
mainSvg.attr("transform", `translate(${margin},0)`); // Shift right to allow for text and margin

// Create a tree layout with specified dimensions
const treeLayout = d3.tree().size([canvasHeight, canvasWidth - margin * 2]); // Adjust width for margin

// Apply the tree layout to the hierarchy data
const treeData = treeLayout(hierarchyData);

// Extract nodes and links from the tree data
const nodes = treeData.descendants();
const links = treeData.links();

// Create links using the tree data
const link = mainSvg
  .selectAll(".link")
  .data(links)
  .enter()
  .append("path")
  .attr("class", "link")
  .attr(
    "d",
    d3
      .linkHorizontal()
      .x((d) => d.y + margin)
      .y((d) => d.x)
  );

// Create nodes
const node = mainSvg
  .selectAll(".node")
  .data(nodes)
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("transform", (d) => `translate(${d.y + margin},${d.x})`);

const getFill = (level) => {
  switch (level) {
    case "Elementary":
      return "#FDB536";
    case "Medium":
      return "#D95561";
    case "Advanced":
      return "#5B9545";
    default:
      return "#FFFFFF";
  }
};

const getStroke = (level) => {
  switch (level) {
    case "Elementary":
      return "#C26C28";
    case "Medium":
      return "#7D3252";
    case "Advanced":
      return "#2D591D";
    default:
      return "#000000";
  }
};

const getLevel = (level) => {
  switch (level) {
    case "Elementary":
      return "HSK 1-3";
    case "Medium":
      return "HSK 4-6";
    case "Advanced":
      return "HSK 7-9";
    default:
      return "#000000";
  }
};

node
  .append("ellipse")
  .attr("rx", (d) => {
    const len = d.data.character.length;
    return len === 1 ? 24 : 14 * (len - 1) + 10;
  }) // Corrected: Radius for the x-axis (width)
  .attr("ry", 24) // Radius for the y-axis (height)
  .style("fill", (d) => getFill(d.data.level))
  .style("stroke", (d) => getStroke(d.data.level)); // Darker stroke for contrast

node
  .append("text")
  .style("font-size", "28px")
  .style("font-family", "Noto Serif CJK SC, HanaMinB")
  .attr("dy", "0.35em") // Vertically centers the text, adjust as needed
  .attr("x", 0) // Centers the text horizontally within the circle
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => d.data.character.replace("囧", "")); // Assuming you want to display the character inside the circle

node
  .append("text")
  .style("font-size", "14px")
  .attr("dy", -32)
  .attr("x", 0)
  .style("fill", (d) => getFill(d.data.level))
  .style("stroke", (d) => getFill(d.data.level))
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => (d.data.level ? ` [${getLevel(d.data.level)}]` : ""));

node
  .append("a")
  .attr("xlink:href", (d) => `./${d.data.filename}.html`) // Replace with your desired URL pattern
  .append("text")
  .style("font-weight", "bold")
  .style("font-family", "Noto Sans CJK SC")
  .attr("dy", 44)
  .attr("x", 0)
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => d.data.keyword + (d.data.number ? `\u00A0(${d.data.number})` : ""));

function countLayerWidths(layer, tree) {
  treeLayerWidths[layer] = (treeLayerWidths[layer] || 0) + 1;
  layer++;
  for (const childNode of tree["requirements"]) {
    countLayerWidths(layer, childNode);
  }
}

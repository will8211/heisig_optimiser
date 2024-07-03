// app.js

// Sample data structure
const data = {
  number: "70",
  character: "的",
  keyword: "bull’s eye",
  level: "Elementary",
  id: "H",
  requirements: [
    {
      number: "34",
      character: "白",
      keyword: "white",
      level: "Elementary",
      id: "D",
      requirements: [
        {
          number: "12",
          character: "日",
          keyword: "day",
          level: "Elementary",
          id: "B",
          requirements: [],
        },
        {
          number: null,
          character: "丶",
          keyword: "a drop of",
          level: null,
          id: "C",
          requirements: [],
        },
      ],
    },
    {
      number: "69",
      character: "勺",
      keyword: "ladle",
      level: "Medium",
      id: "G",
      requirements: [
        {
          number: null,
          character: "勹",
          keyword: "bound up",
          level: null,
          id: "E",
          requirements: [],
        },
        {
          number: null,
          character: "丶",
          keyword: "a drop of",
          level: null,
          id: "F",
          requirements: [],
        },
      ],
    },
  ],
};

// Convert the data into a hierarchy
const hierarchyData = d3.hierarchy(data, (d) => d.requirements);

// Set canvas dimensions
const canvasWidth = 1200;
const canvasHeight = 800;

// Create a tree layout with specified dimensions
const treeLayout = d3.tree().size([canvasHeight, canvasWidth - 160]); // Adjust width for margin

// Apply the tree layout to the hierarchy data
const treeData = treeLayout(hierarchyData);

// Extract nodes and links from the tree data
const nodes = treeData.descendants();
const links = treeData.links();

// Select the body element and append an SVG container
const mainSvg = d3
  .select("body")
  .append("svg")
  .attr("width", canvasWidth)
  .attr("height", canvasHeight);

// Adjust the mainSvg to add some margins
mainSvg.attr("transform", "translate(80,0)"); // Shift right to allow for text and margin

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
      .x((d) => d.y)
      .y((d) => d.x)
  );

// Create nodes
const node = mainSvg
  .selectAll(".node")
  .data(nodes)
  .enter()
  .append("g")
  .attr("class", "node")
  .attr("transform", (d) => `translate(${d.y},${d.x})`);

node
  .append("circle")
  .attr("r", 12)
  .style("fill", "#69b3a2") // Light green fill
  .style("stroke", "#406d80"); // Darker stroke for contrast

node
  .append("text")
  .attr("dy", "0.35em") // Vertically centers the text, adjust as needed
  .attr("x", 0) // Centers the text horizontally within the circle
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => d.data.character); // Assuming you want to display the character inside the circle

node
  .append("text")
  .attr("dy", 3)
  .attr("x", (d) => (d.children ? -15 : 15))
  .style("text-anchor", (d) => (d.children ? "end" : "start"))
  .text((d) => (d.data.keyword + (d.data.number ? ` (${d.data.number})` : "")));

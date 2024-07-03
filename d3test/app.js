// app.js

// Sample data structure
const data = {
  number: "1243",
  character: "睡",
  keyword: "sleep",
  level: "Elementary",
  id: "G",
  requirements: [
    {
      number: "15",
      character: "目",
      keyword: "eye",
      level: "Medium",
      id: "B",
      requirements: [],
    },
    {
      number: "1241",
      character: "垂",
      keyword: "droop",
      level: null,
      id: "F",
      requirements: [
        {
          number: null,
          character: "壬",
          keyword: "porter",
          level: null,
          id: "D",
          requirements: [
            {
              number: "334",
              character: "士",
              keyword: "soldier",
              level: "Advanced",
              id: "C",
              requirements: [],
            },
          ],
        },
        {
          number: null,
          character: "囧垂－一－一",
          keyword: "silage",
          level: null,
          id: "E",
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
  console.log(level);
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
  console.log(level);
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
    return len === 1 ? 16 : 10 * (len - 1);
  }) // Corrected: Radius for the x-axis (width)
  .attr("ry", 16) // Radius for the y-axis (height)
  .style("fill", (d) => getFill(d.data.level))
  .style("stroke", (d) => getStroke(d.data.level)); // Darker stroke for contrast

node
  .append("text")
  .attr("dy", "0.35em") // Vertically centers the text, adjust as needed
  .attr("x", 0) // Centers the text horizontally within the circle
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => d.data.character.replace("囧", "")); // Assuming you want to display the character inside the circle

node
  .append("text")
  .attr("dy", -24)
  .attr("x", 0)
  .style("fill", (d) => getFill(d.data.level))
  .style("stroke", (d) => getFill(d.data.level)) // Darker stroke for contrast
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => (d.data.level ? ` [${getLevel(d.data.level)}]` : ""));

node
  .append("text")
  .attr("dy", 34)
  .attr("x", 0)
  .style("text-anchor", "middle") // Ensures the text is centered horizontally
  .text((d) => d.data.keyword + (d.data.number ? ` (${d.data.number})` : ""));

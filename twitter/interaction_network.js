'use strict'



d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
  };

  d3.selection.prototype.moveToBack = function() {  
        return this.each(function() { 
            var firstChild = this.parentNode.firstChild; 
            if (firstChild) { 
                this.parentNode.insertBefore(this, firstChild); 
            } 
        });
 };


function fixna(x) {
    if (isFinite(x)) return x;
    return 0;
}



async function wrapper(){
	let hname = window.location.search.split("=")[1]
	let data = await d3.json("static_data/" + hname + ".json")
	console.log(data)
	let height = window.innerHeight;
	let width = window.innerWidth;
	let formatter  = d3.format(".3s")


	  $('.mouseover').off()

	let transform = d3.zoomIdentity;
	d3.select("#identifier").text(hname)
	d3.select("#network-size").text(formatter(data.nodes.length))
	let network_svg =  d3.select("#vis-div").append("svg")
							.attr("height", height)
							.attr("width", width)
							.attr("id", "network_svg");

	let nodeExt = d3.extent(data.nodes, function(d){
		return d.score;
	})

	let nodeScale = d3.scaleLinear().domain(nodeExt).range([3, 20])
	let linkExt = d3.extent(data.links, function(d){
		return d.value
	})

	let linkScale = d3.scaleLinear().domain(linkExt).range([1.5, 10])
	const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(function(d){
      	//console.log(d)
      	return d.id
      })
        .distance((d) => 20)//dataObj.linkScale(d.count) )
        .strength((d)=> 1)
      )
      .force("charge", d3.forceManyBody()
        .strength(-100)
      )
       .force('center', d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

const zoomRect = network_svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all")

const linkg = network_svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.5)

    const link = linkg
	    .selectAll("line")
	    .data(data.links)
	    .enter().append("line")
	      .attr("stroke-width", function(d){
	      	return linkScale(d.value)
	      })
	      .attr("class", function(d){
	        return "link_" + d.source.name.replace(/ /g, "_") + " link_" + d.target.name.replace(/ /g, "_")
	      })
	      .on("mouseover", function(d){
	        d3.select(this).attr("stroke-opacity", 1)
	      })
	      .on("mouseout", function(d){
	        d3.select(this).attr("stroke-opacity", .5)
	      })


	const node = network_svg.append("g")
    .attr("id", 'nodes_outer_g')
    .selectAll("g")
    .data(data.nodes)
    .enter().append("g")
    	.attr("class", 'node_g')
    	.attr("id", function(d){
    		return "id_" + d.id
    }).on("mouseover", function(d){
    	d3.selectAll(".line").style("stroke-opacity", .05)
    	
    	/*d3.select(".line_" + d.name).style("stroke-opacity", 1).style("stroke-width", 2.5)
    	d3.select(this).select("circle")
          .style("stroke-width", 5)
    	d3.select(this).select("text")
          .style("font-size", 50)*/
    	highlightEdges(d.id)
    	d3.select(this).moveToFront()

    	$('.mouseover').removeClass('hidden')
       			let mouseloc = d3.mouse(document.getElementById('network_svg'))
       			let data = { left: mouseloc[0] + 25, top: mouseloc[1] + 48}
       			$('.mouseover').offset(data)
       			if(d.text != undefined){
       				$('.name.mousep').text(d.name)
       				$('.count.mousep').text(d.text.toString())
       			}
    	
    })
    .on("mouseout", function(d){
    	d3.selectAll(".line").style("stroke-opacity", .5)
    	
    	//d3.select(".line_" + d.name).style("stroke-width", 1)
    	
    	//d3.select(this).select("text").style("font-size", function(d){
    	//	return Math.max(20, dataObj.nodeScale(d.count))
    	//})
    	//d3.select(this).select("circle").style("stroke-width", 1.5)
    	$('.deselected_node').removeClass('deselected_node')
  		$('.selected_edge').removeClass('selected_edge')
  		d3.select(this).moveToBack()
  		$('.mouseover').addClass('hidden')
    })


node.append("circle")
  	.attr("r", function(d){
 		return nodeScale(d.score)
  	})
  	.attr("stroke", "black")
    .attr("stroke-width", 1.5)
    .attr("fill", function(d){
    	//console.log(d)
    	if (d.nodetype == "searchword"){
    		return searchnodecolor
    	}
    	return "white"
    });


function highlightEdges(id){
  $('.selected_edge').removeClass('selected_edge')
  $('.node_g').addClass("deselected_node")
  $('#' + "id_" + id).removeClass("deselected_node")
  link.attr("class", function(d){
    if(d.target.id == id){
      $('#' + "id_" + d.source.id).removeClass("deselected_node")
      return 'selected_edge'
    }
    else if(d.source.id == id){
      $('#' + "id_" + d.target.id).removeClass("deselected_node")

      return 'selected_edge'
    }
    else{
      return ''
    }
  })

}



const zoom = d3.zoom()
      .scaleExtent([.05, 200])
      .on("zoom", zoomed);

zoomRect.on("click", function(){
    renderTweetTable(dataObj.topTweets, "", searchnodecolor)
  	//$('.deselected_node').removeClass('deselected_node')
  	//$('.selected_edge').removeClass('selected_edge')
  }
  )
zoomRect.call(zoom)
    .call(zoom.scaleTo, .3);

function zoomed() {

    transform = d3.event.transform;
    d3.select('#nodes_outer_g').attr("transform", d3.event.transform);
    link.attr("transform", d3.event.transform);
  }




let tickcount = 0
let maxticks = 50
simulation.on("tick", () => {
  	$('.loading-message').text("Generating network locations " + d3.format('.0%')((tickcount / maxticks)))
  	tickcount += 1
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node.attr("transform", function(d) {
        return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
    });
    if (tickcount >= maxticks){
    	simulation.stop()
    	/*$('.loading-message').text("Finishing up")
    	 $('#loading-div').addClass("hidden")
		$('#vis-div').removeClass("hidden")
		$('#table-div').removeClass("hidden")	*/
    }
  });

}
wrapper()